#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import stat
import sys
from pathlib import Path


BANNED_NAMES = {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"}
SCENE_BANNED_PHRASES = {
    "Planner -> Context Analyst -> Solution Architect -> Implementer -> Reviewer & Tester -> Documenter",
    "任务目录初始化",
    "完成标记写入",
}
SCENE_TRIGGER_REQUIRED_PHRASES = {"use only when", "not for"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_manifest(root: Path) -> dict:
    manifest_path = root / "docs/skills-src/manifest.yaml"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def parse_frontmatter(skill_path: Path) -> dict[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter opening ---")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("missing frontmatter closing ---")
    frontmatter_text = parts[0].split("---\n", 1)[1]
    result: dict[str, str] = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def collect_local_links(skill_path: Path) -> list[str]:
    text = skill_path.read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    return [link for link in links if "://" not in link and not link.startswith("#")]


def is_executable(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IXUSR)


def validate_skill(root: Path, source_root: Path, prompt_root: Path, skill_meta: dict) -> list[str]:
    errors: list[str] = []
    skill_id = skill_meta["id"]
    skill_dir = source_root / skill_id
    skill_file = skill_dir / "SKILL.md"

    required_paths = [
        skill_file,
        skill_dir / "references/workflow.md",
        skill_dir / "references/output-contract.md",
        skill_dir / "references/checklists.md",
        skill_dir / "agents/openai.yaml",
    ]
    required_paths.extend(skill_dir / rel for rel in skill_meta.get("expectedScripts", []))
    required_paths.extend(skill_dir / rel for rel in skill_meta.get("expectedAssets", []))

    for path in required_paths:
        if not path.exists():
            errors.append(f"{skill_id}: missing required path {path.relative_to(root)}")

    for rel in skill_meta.get("expectedScripts", []):
        script_path = skill_dir / rel
        if script_path.exists() and not is_executable(script_path):
            errors.append(f"{skill_id}: script must be executable {script_path.relative_to(root)}")

    if not skill_file.exists():
        return errors

    try:
        frontmatter = parse_frontmatter(skill_file)
    except ValueError as exc:
        errors.append(f"{skill_id}: {exc}")
        return errors

    if frontmatter.get("name") != skill_id:
        errors.append(f"{skill_id}: frontmatter name must equal directory name")
    if not frontmatter.get("description"):
        errors.append(f"{skill_id}: frontmatter description is required")

    for link in collect_local_links(skill_file):
        if not (skill_dir / link).exists():
            errors.append(f"{skill_id}: broken local link {link}")

    openai_yaml = skill_dir / "agents/openai.yaml"
    if openai_yaml.exists():
        openai_text = openai_yaml.read_text(encoding="utf-8")
        for required_key in ("display_name:", "short_description:", "default_prompt:"):
            if required_key not in openai_text:
                errors.append(f"{skill_id}: agents/openai.yaml missing {required_key}")

    for path in skill_dir.rglob("*"):
        if path.is_file() and path.name in BANNED_NAMES:
            errors.append(f"{skill_id}: contains banned auxiliary file {path.name}")

    positives = skill_meta.get("positiveExamples", [])
    negatives = skill_meta.get("negativeExamples", [])
    if len(positives) < 2 or len(negatives) < 1:
        errors.append(f"{skill_id}: requires at least 2 positiveExamples and 1 negativeExamples in manifest")

    for prompt_name in skill_meta.get("compatPrompts", []):
        prompt_path = prompt_root / prompt_name
        if not prompt_path.exists():
            errors.append(f"{skill_id}: compat prompt missing {prompt_name}")

    if skill_meta["type"] == "scene":
        skill_text = skill_file.read_text(encoding="utf-8")
        description_lower = frontmatter["description"].lower()
        for core_ref in skill_meta.get("requiredCoreRefs", []):
            if core_ref not in skill_text:
                errors.append(f"{skill_id}: scene skill must reference core skill {core_ref}")
        for phrase in SCENE_BANNED_PHRASES:
            if phrase in skill_text:
                errors.append(f"{skill_id}: scene skill repeats core flow phrase '{phrase}'")
        for phrase in SCENE_TRIGGER_REQUIRED_PHRASES:
            if phrase not in description_lower:
                errors.append(f"{skill_id}: scene skill description must contain trigger hygiene phrase '{phrase}'")

    return errors


def main() -> int:
    root = repo_root()
    manifest = load_manifest(root)
    source_root = root / manifest["sourceRoot"]
    prompt_root = root / manifest["promptRoot"]

    all_errors: list[str] = []
    seen_ids: set[str] = set()

    for skill_meta in manifest["skills"]:
        skill_id = skill_meta["id"]
        if skill_id in seen_ids:
            all_errors.append(f"duplicate skill id in manifest: {skill_id}")
            continue
        seen_ids.add(skill_id)
        all_errors.extend(validate_skill(root, source_root, prompt_root, skill_meta))

    if all_errors:
        print("[FAIL] Skill validation failed:")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print(f"[OK] Skill validation passed for {len(manifest['skills'])} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
