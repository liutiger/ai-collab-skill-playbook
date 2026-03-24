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
    matches = re.findall(r"第(\d+)次(?:提交|补充)(?:已完成)?", text)
    if not matches:
        return 1
    return max(int(item) for item in matches) + 1


def planning_section_bounds(lines: list[str]) -> tuple[int, int, bool]:
    heading = "## 任务提交记录"
    heading_index = next((idx for idx, line in enumerate(lines) if line.strip() == heading), None)
    if heading_index is not None:
        end_index = len(lines)
        for idx in range(heading_index + 1, len(lines)):
            if lines[idx].startswith("## "):
                end_index = idx
                break
        return heading_index, end_index, True

    insert_index = next((idx for idx, line in enumerate(lines) if line.startswith("## ")), len(lines))
    return insert_index, insert_index, False


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a standardized planning marker to a task README.")
    parser.add_argument("readme", help="Path to README.md")
    parser.add_argument("summary", help="Planning summary to write in the marker")
    parser.add_argument("--iteration", type=int, help="Explicit iteration number")
    parser.add_argument("--user", help="Explicit git username")
    parser.add_argument(
        "--kind",
        choices=("提交", "补充"),
        default="提交",
        help="Marker kind. Use 补充 for follow-up requirement additions.",
    )
    args = parser.parse_args()

    readme_path = Path(args.readme).resolve()
    text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    iteration = args.iteration or next_iteration(text)
    user = args.user or git_user(readme_path)
    now = datetime.now()
    stamp = f"{now:%y}年{now.month}月{now.day}日 {now:%H:%M:%S}"
    marker = f"---- {stamp} ，第{iteration}次{args.kind} ，提交人：{user} ，规划任务: {args.summary}"

    lines = text.splitlines()
    start, end, has_section = planning_section_bounds(lines)

    if has_section:
        insert_lines = [marker, ""]
        lines[start + 1 : end] = lines[start + 1 : end] + insert_lines
    else:
        section = ["## 任务提交记录", "", marker, ""]
        lines[start:start] = section

    readme_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"[OK] Appended planning marker to {readme_path} (iteration={iteration}, kind={args.kind})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
