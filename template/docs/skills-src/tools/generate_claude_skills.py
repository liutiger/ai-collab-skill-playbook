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


def file_hash(path: Path) -> bytes:
    return path.read_bytes()


def executable_flag(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IXUSR)


def same_file(source: Path, target: Path) -> bool:
    return file_hash(source) == file_hash(target) and executable_flag(source) == executable_flag(target)


def list_files(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    return {
        str(path.relative_to(root)).replace("\\", "/"): path
        for path in root.rglob("*")
        if path.is_file()
    }


def compare_trees(source_root: Path, target_root: Path) -> tuple[list[str], list[str], list[str]]:
    source_files = list_files(source_root)
    target_files = list_files(target_root)

    missing = sorted(rel for rel in source_files if rel not in target_files)
    changed = sorted(
        rel
        for rel in source_files
        if rel in target_files and not same_file(source_files[rel], target_files[rel])
    )
    stale = sorted(rel for rel in target_files if rel not in source_files)
    return missing, changed, stale


def sync_trees(source_root: Path, target_root: Path, clean_stale: bool) -> tuple[list[str], list[str], list[str]]:
    source_files = list_files(source_root)
    target_files = list_files(target_root)

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
    parser.add_argument("--clean-stale", action="store_true", help="Remove files in target that no longer exist in source.")
    args = parser.parse_args()

    root = repo_root()
    manifest = load_manifest(root)
    source_root = root / manifest["sourceRoot"]
    target_root = root / manifest["targetRoot"]

    if not source_root.exists():
        print(f"[ERROR] Source root not found: {source_root}")
        return 1

    missing, changed, stale = compare_trees(source_root, target_root)

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
    created, updated, removed = sync_trees(source_root, target_root, clean_stale=args.clean_stale)

    print("[OK] Skill generation completed.")
    print(f"  Source: {source_root}")
    print(f"  Target: {target_root}")
    print(f"  Created: {len(created)}")
    print(f"  Updated: {len(updated)}")
    print(f"  Removed: {len(removed)}")

    if stale and not args.clean_stale:
        print("  Note: stale files remain in target. Re-run with --clean-stale to remove them.")

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
