#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_manifest(root: Path) -> dict:
    manifest_path = root / "docs/skills-src/manifest.yaml"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def run_check(command: list[str], root: Path) -> tuple[bool, str]:
    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def main() -> int:
    root = repo_root()
    manifest = load_manifest(root)
    target_root = root / manifest["targetRoot"]
    prompt_root = root / manifest["promptRoot"]
    fixture_metas = manifest.get("manualAcceptanceFixtures", [])
    known_skill_ids = {skill["id"] for skill in manifest["skills"]}

    checks: list[tuple[str, bool, str]] = []

    ok, output = run_check([sys.executable, "docs/skills-src/tools/validate_skills.py"], root)
    checks.append(("validate_skills", ok, output))

    ok, output = run_check([sys.executable, "docs/skills-src/tools/validate_copilot_assets.py"], root)
    checks.append(("validate_copilot_assets", ok, output))

    ok, output = run_check([sys.executable, "docs/skills-src/tools/generate_claude_skills.py", "--check"], root)
    checks.append(("generate_check", ok, output))

    ok, output = run_check([sys.executable, "docs/skills-src/tools/generate_copilot_assets.py", "--check"], root)
    checks.append(("copilot_generate_check", ok, output))

    skill_dirs = sorted(path.name for path in target_root.iterdir() if path.is_dir()) if target_root.exists() else []
    expected_ids = sorted(
        skill["id"] for skill in manifest["skills"] if skill.get("runtimeExposure", "active") == "active"
    )
    checks.append(
        (
            "generated_skill_count",
            skill_dirs == expected_ids,
            f"expected={expected_ids} actual={skill_dirs}",
        )
    )

    scene_exposures_ok = all(
        skill.get("runtimeExposure") == "source-only"
        for skill in manifest["skills"]
        if skill["type"] == "scene"
    )
    checks.append(
        (
            "scene_runtime_exposure",
            scene_exposures_ok,
            "scene skills stay source-only to avoid runtime trigger interference",
        )
    )

    for skill_meta in manifest["skills"]:
        prompt_hits = []
        for prompt_name in skill_meta.get("compatPrompts", []):
            prompt_path = prompt_root / prompt_name
            text = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
            prompt_hits.append(skill_meta["id"] in text)
        checks.append(
            (
                f"compat_prompt_{skill_meta['id']}",
                all(prompt_hits),
                f"compatPrompts={skill_meta.get('compatPrompts', [])}",
            )
        )

        positives = len(skill_meta.get("positiveExamples", [])) >= 2
        negatives = len(skill_meta.get("negativeExamples", [])) >= 1
        checks.append(
            (
                f"examples_{skill_meta['id']}",
                positives and negatives,
                f"positive={len(skill_meta.get('positiveExamples', []))} negative={len(skill_meta.get('negativeExamples', []))}",
            )
        )

    copilot = manifest.get("copilot", {})
    copilot_target_root = root / copilot.get("targetRoot", ".github")
    prompt_specs = copilot.get("promptFiles", [])
    prompt_files = sorted(path.name for path in (copilot_target_root / "prompts").glob("*.prompt.md"))
    expected_prompt_files = sorted(Path(item["filename"]).name for item in prompt_specs)
    checks.append(
        (
            "copilot_prompt_count",
            prompt_files == expected_prompt_files,
            f"expected={expected_prompt_files} actual={prompt_files}",
        )
    )

    repo_instructions_path = copilot_target_root / "copilot-instructions.md"
    repo_text = repo_instructions_path.read_text(encoding="utf-8") if repo_instructions_path.exists() else ""
    checks.append(
        (
            "copilot_repo_instructions_exists",
            repo_instructions_path.exists(),
            str(repo_instructions_path.relative_to(root)),
        )
    )
    checks.append(
        (
            "copilot_repo_mentions_slash_prompts",
            all(f"/{item['id']}" in repo_text for item in prompt_specs),
            "slash prompts listed in repository instructions",
        )
    )
    checks.append(
        (
            "copilot_repo_mentions_charter",
            "AI协作研发章程" in repo_text,
            "repository instructions anchored to charter",
        )
    )
    auto_dev_path = copilot_target_root / "prompts/wms-auto-dev.prompt.md"
    auto_dev_text = auto_dev_path.read_text(encoding="utf-8") if auto_dev_path.exists() else ""
    checks.append(
        (
            "copilot_auto_dev_scene_guard",
            "章程标准场景" in auto_dev_text and "高风险条件" in auto_dev_text and "待人工确认后再实现" in auto_dev_text,
            "auto-dev prompt enforces scene selection and plan gate",
        )
    )
    plan_gate_path = copilot_target_root / "prompts/wms-plan-gate.prompt.md"
    plan_gate_text = plan_gate_path.read_text(encoding="utf-8") if plan_gate_path.exists() else ""
    checks.append(
        (
            "copilot_plan_gate_scene_guard",
            "章程标准场景" in plan_gate_text and "停在待确认" in plan_gate_text and "高风险条件" in plan_gate_text,
            "plan-gate prompt enforces scene selection and hold",
        )
    )
    feature_dev_path = copilot_target_root / "prompts/wms-feature-dev.prompt.md"
    feature_dev_text = feature_dev_path.read_text(encoding="utf-8") if feature_dev_path.exists() else ""
    checks.append(
        (
            "copilot_feature_dev_risk_guard",
            "高风险条件" in feature_dev_text and "plan-gate 风格" in feature_dev_text,
            "feature-dev prompt redirects risky tasks to plan gate",
        )
    )
    evaluation_gate_path = copilot_target_root / "prompts/wms-evaluation-gate.prompt.md"
    evaluation_gate_text = evaluation_gate_path.read_text(encoding="utf-8") if evaluation_gate_path.exists() else ""
    checks.append(
        (
            "copilot_evaluation_gate_guard",
            "PASS / CONDITIONAL_PASS / BLOCKED / FAIL" in evaluation_gate_text
            and "不得写完成标记" in evaluation_gate_text,
            "evaluation-gate prompt enforces verdict and completion guard",
        )
    )
    checks.append(
        (
            "copilot_auto_dev_eval_gate",
            "评测门禁" in auto_dev_text and "完成标记" in auto_dev_text,
            "auto-dev prompt includes evaluation gate before completion",
        )
    )

    checks.append(
        (
            "manual_fixture_count",
            len(fixture_metas) >= 5,
            f"fixtureCount={len(fixture_metas)}",
        )
    )

    for fixture_meta in fixture_metas:
        fixture_path = root / fixture_meta["file"]
        if not fixture_path.exists():
            checks.append((f"manual_fixture_{fixture_meta['id']}", False, f"missing={fixture_meta['file']}"))
            continue

        try:
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            checks.append((f"manual_fixture_{fixture_meta['id']}", False, f"invalid json: {exc}"))
            continue

        skills = fixture.get("skills", [])
        expected_focus = fixture.get("expectedFocus", [])
        expected_artifacts = fixture.get("expectedArtifacts", [])
        fixture_ok = (
            fixture.get("id") == fixture_meta["id"]
            and bool(fixture.get("title"))
            and bool(fixture.get("prompt"))
            and isinstance(skills, list)
            and len(skills) >= 1
            and all(skill_id in known_skill_ids for skill_id in skills)
            and isinstance(expected_focus, list)
            and len(expected_focus) >= 2
            and isinstance(expected_artifacts, list)
            and len(expected_artifacts) >= 1
        )
        checks.append(
            (
                f"manual_fixture_{fixture_meta['id']}",
                fixture_ok,
                f"skills={skills} expectedFocus={len(expected_focus)} expectedArtifacts={len(expected_artifacts)}",
            )
        )

    failures = [item for item in checks if not item[1]]

    if failures:
        print("[FAIL] Acceptance checks failed:")
        for name, _, detail in failures:
            print(f"  - {name}: {detail}")
        return 1

    print("[OK] Acceptance checks passed:")
    for name, _, detail in checks:
        print(f"  - {name}: {detail or 'passed'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
