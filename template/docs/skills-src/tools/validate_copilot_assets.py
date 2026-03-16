#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_manifest(root: Path) -> dict:
    manifest_path = root / "docs/skills-src/manifest.yaml"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    result: dict[str, str] = {}
    for raw_line in parts[0].splitlines()[1:]:
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def main() -> int:
    root = repo_root()
    manifest = load_manifest(root)
    copilot = manifest.get("copilot")
    if not copilot:
        print("[FAIL] Missing copilot section in manifest.")
        return 1

    source_root = root / copilot["sourceRoot"]
    errors: list[str] = []

    repo_source = source_root / copilot["repoInstructionsSource"]
    if not repo_source.exists():
        errors.append(f"missing repo instructions source: {repo_source.relative_to(root)}")
    else:
        repo_text = repo_source.read_text(encoding="utf-8")
        for placeholder in ("{{ROUTING_TABLE}}", "{{PROMPT_TABLE}}", "{{PATH_INSTRUCTION_TABLE}}"):
            if placeholder not in repo_text:
                errors.append(f"repo instructions source missing placeholder {placeholder}")

    instruction_targets: set[str] = set()
    for item in copilot.get("instructions", []):
        src = source_root / item["source"]
        if not src.exists():
            errors.append(f"missing instruction source: {src.relative_to(root)}")
            continue
        target = item["target"]
        if target in instruction_targets:
            errors.append(f"duplicate copilot instruction target: {target}")
        instruction_targets.add(target)
        frontmatter = parse_frontmatter(src.read_text(encoding="utf-8"))
        if "applyTo" not in frontmatter:
            errors.append(f"instruction source missing applyTo frontmatter: {src.relative_to(root)}")

    prompt_ids: set[str] = set()
    filenames: set[str] = set()
    prompt_root = root / manifest["promptRoot"]
    for spec in copilot.get("promptFiles", []):
        if spec["id"] in prompt_ids:
            errors.append(f"duplicate copilot prompt id: {spec['id']}")
        prompt_ids.add(spec["id"])

        filename = spec["filename"]
        if filename in filenames:
            errors.append(f"duplicate copilot prompt filename: {filename}")
        filenames.add(filename)
        if not filename.endswith(".prompt.md"):
            errors.append(f"copilot prompt must end with .prompt.md: {filename}")
        if not spec.get("description"):
            errors.append(f"{spec['id']}: description is required")
        if len(spec.get("triggers", [])) < 2:
            errors.append(f"{spec['id']}: requires at least 2 triggers")
        if len(spec.get("requirements", [])) < 2:
            errors.append(f"{spec['id']}: requires at least 2 requirements")
        if not spec.get("refs"):
            errors.append(f"{spec['id']}: refs are required")
        for ref in spec.get("refs", []):
            if not (root / ref).exists():
                errors.append(f"{spec['id']}: missing referenced prompt {ref}")
            elif not str((root / ref).relative_to(prompt_root.parent)).startswith("prompts/"):
                errors.append(f"{spec['id']}: referenced file must live under docs/prompts: {ref}")

    if errors:
        print("[FAIL] Copilot asset validation failed:")
        for item in errors:
            print(f"  - {item}")
        return 1

    print(
        f"[OK] Copilot asset validation passed for {len(copilot.get('promptFiles', []))} prompt files and "
        f"{len(copilot.get('instructions', []))} path instructions."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
