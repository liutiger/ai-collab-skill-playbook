#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def prompt_kind_label(kind: str) -> str:
    return {
        "router": "总控",
        "gate": "门禁",
        "method": "专项方法",
        "mode": "模式",
    }.get(kind, kind)


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def render_numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def render_prompt_table(prompt_specs: list[dict], shared_refs: list[str]) -> str:
    rows = []
    for spec in prompt_specs:
        command = f"`/{spec['id']}`"
        kind = prompt_kind_label(spec.get("kind", "gate"))
        desc = spec["description"]
        refs = " + ".join(f"`{Path(ref).name}`" for ref in dedupe_preserve_order([*shared_refs, *spec["refs"]]))
        rows.append([kind, command, desc, refs])
    return render_markdown_table(["分类", "Slash Prompt", "用途", "兼容入口"], rows)


def render_routing_table(prompt_specs: list[dict]) -> str:
    rows = []
    for spec in prompt_specs:
        trigger_text = " / ".join(f"`{item}`" for item in spec["triggers"])
        route_text = f"`/{spec['id']}`"
        kind = prompt_kind_label(spec.get("kind", "gate"))
        rows.append([kind, trigger_text, route_text, spec["description"]])
    return render_markdown_table(["分类", "用户信号", "优先工作流", "说明"], rows)


def render_path_instruction_table(instructions: list[dict]) -> str:
    rows = []
    for item in instructions:
        target = f"`{item['target']}`"
        source_name = Path(item["source"]).name
        rows.append([target, f"`{source_name}`"])
    return render_markdown_table(["运行产物", "源码"], rows)


def render_prompt_file(spec: dict, shared_refs: list[str], shared_requirements: list[str]) -> str:
    refs = dedupe_preserve_order([*shared_refs, *spec["refs"]])
    refs_text = "\n".join(f"#file:{ref}" for ref in refs)
    lifecycle_requirements = render_numbered(shared_requirements)
    entry_requirements = render_numbered(spec.get("requirements", []))
    return (
        f"---\n"
        f"description: {json.dumps(spec['description'], ensure_ascii=False)}\n"
        f"---\n\n"
        f"{refs_text}\n\n"
        f"任务：\n"
        f"${{input:task:描述本次任务、异常或改动目标}}\n\n"
        f"补充信息：\n"
        f"${{input:extra:补充验收标准、日志、范围、风险点或可留空}}\n\n"
        f"共享治理生命周期合同：\n"
        f"{lifecycle_requirements}\n\n"
        f"本入口专项要求：\n"
        f"{entry_requirements}\n"
    )


def expected_files(root: Path, manifest: dict) -> dict[str, bytes]:
    copilot = manifest["copilot"]
    source_root = root / copilot["sourceRoot"]
    repo_source = source_root / copilot["repoInstructionsSource"]
    prompt_specs = copilot["promptFiles"]
    instruction_specs = copilot["instructions"]
    shared_refs = copilot.get("sharedRefs", [])
    shared_requirements = copilot.get("sharedRequirements", [])

    repo_text = repo_source.read_text(encoding="utf-8")
    repo_text = repo_text.replace("{{ROUTING_TABLE}}", render_routing_table(prompt_specs))
    repo_text = repo_text.replace("{{PROMPT_TABLE}}", render_prompt_table(prompt_specs, shared_refs))
    repo_text = repo_text.replace("{{PATH_INSTRUCTION_TABLE}}", render_path_instruction_table(instruction_specs))

    files: dict[str, bytes] = {"copilot-instructions.md": repo_text.encode("utf-8")}

    for item in instruction_specs:
        rel_target = item["target"]
        files[rel_target] = (source_root / item["source"]).read_bytes()

    for spec in prompt_specs:
        files[spec["filename"]] = render_prompt_file(spec, shared_refs, shared_requirements).encode("utf-8")

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

        for directory_name in ("prompts", "instructions"):
            directory = target_root / directory_name
            if not directory.exists():
                continue
            for path in sorted(directory.rglob("*"), reverse=True):
                if path.is_dir() and not any(path.iterdir()):
                    path.rmdir()

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
        print("  Hint: rerun with --clean-stale to remove obsolete generated files.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
