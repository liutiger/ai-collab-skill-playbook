#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import stat
import shutil
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_manifest(root: Path) -> dict:
    manifest_path = root / "docs/skills-src/manifest.yaml"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def active_skill_ids(manifest: dict) -> list[str]:
    return [
        skill["id"]
        for skill in manifest["skills"]
        if skill.get("runtimeExposure", "active") == "active"
    ]


def file_hash(path: Path) -> bytes:
    return path.read_bytes()


def executable_flag(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IXUSR)


def same_file(source: Path, target: Path) -> bool:
    return file_hash(source) == file_hash(target) and executable_flag(source) == executable_flag(target)


def source_files_for_active_skills(source_root: Path, skill_ids: list[str]) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for skill_id in skill_ids:
        skill_root = source_root / skill_id
        if not skill_root.exists():
            continue
        for path in skill_root.rglob("*"):
            if path.is_file():
                rel = str(path.relative_to(source_root)).replace("\\", "/")
                files[rel] = path
    return files


def list_target_files(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    return {
        str(path.relative_to(root)).replace("\\", "/"): path
        for path in root.rglob("*")
        if path.is_file()
    }


def compare_trees(source_files: dict[str, Path], target_root: Path) -> tuple[list[str], list[str], list[str]]:
    target_files = list_target_files(target_root)
    missing = sorted(rel for rel in source_files if rel not in target_files)
    changed = sorted(
        rel
        for rel in source_files
        if rel in target_files and not same_file(source_files[rel], target_files[rel])
    )
    stale = sorted(rel for rel in target_files if rel not in source_files)
    return missing, changed, stale


def sync_trees(source_files: dict[str, Path], target_root: Path, clean_stale: bool) -> tuple[list[str], list[str], list[str]]:
    target_files = list_target_files(target_root)
    created: list[str] = []
    updated: list[str] = []
    removed: list[str] = []

    for rel, src in source_files.items():
        dst = target_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(src, dst)
            created.append(rel)
            continue
        if not same_file(src, dst):
            shutil.copy2(src, dst)
            updated.append(rel)

    if clean_stale:
        for rel, dst in sorted(target_files.items(), reverse=True):
            if rel not in source_files:
                dst.unlink()
                removed.append(rel)
        for directory in sorted(target_root.rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()

    return created, updated, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate .claude/skills/wms from docs/skills-src.")
    parser.add_argument("--check", action="store_true", help="Only check whether source and target are in sync.")
    parser.add_argument("--clean-stale", action="store_true", help="Deprecated alias; stale runtime skill files are removed by default.")
    parser.add_argument("--no-clean-stale", action="store_true", help="Keep stale files in target instead of removing them.")
    args = parser.parse_args()

    root = repo_root()
    manifest = load_manifest(root)
    source_root = root / manifest["sourceRoot"]
    target_root = root / manifest["targetRoot"]
    selected_skill_ids = active_skill_ids(manifest)
    source_files = source_files_for_active_skills(source_root, selected_skill_ids)

    if not source_root.exists():
        print(f"[ERROR] Source root not found: {source_root}")
        return 1

    missing, changed, stale = compare_trees(source_files, target_root)

    if args.check:
        if not missing and not changed and not stale:
            print("[OK] Skill source and target are in sync.")
            return 0
        print("[DIFF] Skill source and target are not in sync.")
        if missing:
            print("  Missing in target:")
            for item in missing:
                print(f"    - {item}")
        if changed:
            print("  Changed:")
            for item in changed:
                print(f"    - {item}")
        if stale:
            print("  Stale in target:")
            for item in stale:
                print(f"    - {item}")
        return 1

    target_root.mkdir(parents=True, exist_ok=True)
    clean_stale = not args.no_clean_stale
    created, updated, removed = sync_trees(source_files, target_root, clean_stale=clean_stale)

    print("[OK] Skill generation completed.")
    print(f"  Source: {source_root}")
    print(f"  Target: {target_root}")
    print(f"  Active runtime skills: {selected_skill_ids}")
    print(f"  Created: {len(created)}")
    print(f"  Updated: {len(updated)}")
    print(f"  Removed: {len(removed)}")

    if stale and not clean_stale:
        print("  Note: stale files remain in target because --no-clean-stale was used.")

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
