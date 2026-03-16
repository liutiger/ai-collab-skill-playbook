#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path


def git_user(readme_path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(readme_path.parent), "config", "user.name"],
        capture_output=True,
        text=True,
        check=False,
    )
    user = result.stdout.strip()
    return user or "unknown"


def next_iteration(text: str) -> int:
    matches = re.findall(r"第(\d+)次提交已完成", text)
    if not matches:
        return 1
    return max(int(item) for item in matches) + 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a standardized completion marker to a task README.")
    parser.add_argument("readme", help="Path to README.md")
    parser.add_argument("summary", help="Result summary to write before the marker")
    parser.add_argument("--iteration", type=int, help="Explicit iteration number")
    parser.add_argument("--user", help="Explicit git username")
    args = parser.parse_args()

    readme_path = Path(args.readme).resolve()
    text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    iteration = args.iteration or next_iteration(text)
    user = args.user or git_user(readme_path)
    now = datetime.now()
    stamp = f"{now:%y}年{now.month}月{now.day}日 {now:%H:%M:%S}"

    block = (
        f"\n任务处理结果: {args.summary}\n\n"
        f"----{stamp} 第{iteration}次提交已完成，提交人：{user}----\n"
    )
    if text and not text.endswith("\n"):
        text += "\n"
    readme_path.write_text(text + block, encoding="utf-8")
    print(f"[OK] Appended completion marker to {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
