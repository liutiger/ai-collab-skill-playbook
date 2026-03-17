#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_manifest(root: Path) -> dict:
    manifest_path = root / "docs/skills-src/manifest.yaml"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def render_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "|" + "|".join(["---"] * len(headers)) + "|"
    body_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, separator_row, *body_rows])


def render_prompt_table(prompt_specs: list[dict]) -> str:
    rows = []
    for spec in prompt_specs:
        command = f"`/{spec['id']}`"
        desc = spec["description"]
        refs = " + ".join(f"`{Path(ref).name}`" for ref in spec["refs"])
        rows.append([command, desc, refs])
    return render_markdown_table(["Slash Prompt", "用途", "兼容入口"], rows)


def render_routing_table(prompt_specs: list[dict]) -> str:
    rows = []
    for spec in prompt_specs:
        trigger_text = " / ".join(f"`{item}`" for item in spec["triggers"])
        route_text = f"`/{spec['id']}`"
        rows.append([trigger_text, route_text, spec["description"]])
    return render_markdown_table(["用户信号", "优先工作流", "说明"], rows)


def render_path_instruction_table(instructions: list[dict]) -> str:
    rows = []
    for item in instructions:
        target = f"`{item['target']}`"
        source_name = Path(item["source"]).name
        rows.append([target, f"`{source_name}`"])
    return render_markdown_table(["运行产物", "源码"], rows)


def render_prompt_file(spec: dict) -> str:
    refs = "\n".join(f"#file:{ref}" for ref in spec["refs"])
    requirements = "\n".join(
        f"{index}. {item}" for index, item in enumerate(spec.get("requirements", []), start=1)
    )
    return (
        f"---\n"
        f"description: {json.dumps(spec['description'], ensure_ascii=False)}\n"
        f"---\n\n"
        f"{refs}\n\n"
        f"任务：\n"
        f"${{input:task:描述本次任务、异常或改动目标}}\n\n"
        f"补充信息：\n"
        f"${{input:extra:补充验收标准、日志、范围、风险点或可留空}}\n\n"
        f"执行要求：\n"
        f"{requirements}\n"
    )


def expected_files(root: Path, manifest: dict) -> dict[str, bytes]:
    copilot = manifest["copilot"]
    source_root = root / copilot["sourceRoot"]
    repo_source = source_root / copilot["repoInstructionsSource"]
    prompt_specs = copilot["promptFiles"]
    instruction_specs = copilot["instructions"]

    repo_text = repo_source.read_text(encoding="utf-8")
    repo_text = repo_text.replace("{{ROUTING_TABLE}}", render_routing_table(prompt_specs))
    repo_text = repo_text.replace("{{PROMPT_TABLE}}", render_prompt_table(prompt_specs))
    repo_text = repo_text.replace("{{PATH_INSTRUCTION_TABLE}}", render_path_instruction_table(instruction_specs))

    files: dict[str, bytes] = {"copilot-instructions.md": repo_text.encode("utf-8")}

    for item in instruction_specs:
        rel_target = item["target"]
        files[rel_target] = (source_root / item["source"]).read_bytes()

    for spec in prompt_specs:
        files[spec["filename"]] = render_prompt_file(spec).encode("utf-8")

    inventory_rel = copilot["inventoryFile"]
    inventory = {"managedPaths": sorted(files.keys())}
    files[inventory_rel] = (json.dumps(inventory, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return files


def load_inventory(target_root: Path, inventory_rel: str) -> list[str]:
    inventory_path = target_root / inventory_rel
    if not inventory_path.exists():
        return []
    try:
        data = json.loads(inventory_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    managed_paths = data.get("managedPaths", [])
    return [item for item in managed_paths if isinstance(item, str)]


def discover_generated_paths(target_root: Path) -> list[str]:
    discovered: set[str] = set()
    for directory_name in ("prompts", "instructions"):
        directory = target_root / directory_name
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file():
                discovered.add(str(path.relative_to(target_root)))
    repo_instructions = target_root / "copilot-instructions.md"
    if repo_instructions.exists():
        discovered.add(str(repo_instructions.relative_to(target_root)))
    return sorted(discovered)


def compare(expected: dict[str, bytes], target_root: Path, inventory_rel: str) -> tuple[list[str], list[str], list[str]]:
    missing: list[str] = []
    changed: list[str] = []
    stale: list[str] = []

    for rel, expected_bytes in expected.items():
        path = target_root / rel
        if not path.exists():
            missing.append(rel)
            continue
        if path.read_bytes() != expected_bytes:
            changed.append(rel)

    previous_managed = set(load_inventory(target_root, inventory_rel))
    discovered_paths = set(discover_generated_paths(target_root))
    expected_keys = set(expected)
    for rel in sorted(previous_managed | discovered_paths):
        if rel not in expected_keys and (target_root / rel).exists():
            stale.append(rel)

    return sorted(missing), sorted(changed), sorted(stale)


def sync(expected: dict[str, bytes], target_root: Path, inventory_rel: str, clean_stale: bool) -> tuple[list[str], list[str], list[str]]:
    created: list[str] = []
    updated: list[str] = []
    removed: list[str] = []
    previous_managed = set(load_inventory(target_root, inventory_rel))
    discovered_paths = set(discover_generated_paths(target_root))

    for rel, data in expected.items():
        path = target_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(data)
            created.append(rel)
            continue
        if path.read_bytes() != data:
            path.write_bytes(data)
            updated.append(rel)

    if clean_stale:
        for rel in sorted(previous_managed | discovered_paths):
            if rel in expected:
                continue
            path = target_root / rel
            if path.exists():
                path.unlink()
                removed.append(rel)

        for directory in sorted((target_root / "prompts").rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
        for directory in sorted((target_root / "instructions").rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()

    return created, updated, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate GitHub Copilot assets from docs/skills-src.")
    parser.add_argument("--check", action="store_true", help="Only check whether source and target are in sync.")
    parser.add_argument("--clean-stale", action="store_true", help="Remove stale generated files tracked in inventory.")
    args = parser.parse_args()

    root = repo_root()
    manifest = load_manifest(root)
    copilot = manifest["copilot"]
    target_root = root / copilot["targetRoot"]
    inventory_rel = copilot["inventoryFile"]

    expected = expected_files(root, manifest)
    missing, changed, stale = compare(expected, target_root, inventory_rel)

    if args.check:
        if not missing and not changed and not stale:
            print("[OK] Copilot source and target are in sync.")
            return 0
        print("[DIFF] Copilot source and target are not in sync.")
        if missing:
            print("  Missing in target:")
            for item in missing:
                print(f"    - {item}")
        if changed:
            print("  Changed:")
            for item in changed:
                print(f"    - {item}")
        if stale:
            print("  Stale managed files:")
            for item in stale:
                print(f"    - {item}")
        return 1

    target_root.mkdir(parents=True, exist_ok=True)
    created, updated, removed = sync(expected, target_root, inventory_rel, clean_stale=args.clean_stale)

    print("[OK] Copilot asset generation completed.")
    print(f"  Target: {target_root}")
    print(f"  Created: {len(created)}")
    print(f"  Updated: {len(updated)}")
    print(f"  Removed: {len(removed)}")

    if stale and not args.clean_stale:
        print("  Note: stale managed files remain. Re-run with --clean-stale to remove them.")
    if created:
        print("  Created files:")
        for item in created:
            print(f"    - {item}")
    if updated:
        print("  Updated files:")
        for item in updated:
            print(f"    - {item}")
    if removed:
        print("  Removed files:")
        for item in removed:
            print(f"    - {item}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
