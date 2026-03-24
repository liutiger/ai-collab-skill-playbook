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
    strategy_exposures_ok = all(
        skill.get("runtimeExposure") == "source-only"
        for skill in manifest["skills"]
        if skill["type"] == "strategy"
    )
    checks.append(("scene_runtime_exposure", scene_exposures_ok, "scene skills stay source-only"))
    checks.append(("strategy_runtime_exposure", strategy_exposures_ok, "strategy packs stay source-only"))

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
    shared_refs = copilot.get("sharedRefs", [])
    shared_requirements = copilot.get("sharedRequirements", [])
    docs_tasks_instruction_path = copilot_target_root / "instructions/docs-tasks.instructions.md"
    docs_tasks_instruction_text = (
        docs_tasks_instruction_path.read_text(encoding="utf-8") if docs_tasks_instruction_path.exists() else ""
    )

    checks.append(("copilot_repo_instructions_exists", repo_instructions_path.exists(), str(repo_instructions_path.relative_to(root))))
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
    checks.append(
        (
            "copilot_shared_lifecycle_contract",
            "docs/prompts/15-governance-lifecycle-contract.md" in shared_refs
            and any("规划任务" in item for item in shared_requirements)
            and any("继续检查文档" in item for item in shared_requirements),
            "copilot manifest declares shared lifecycle refs and requirements",
        )
    )
    governance_prompt_path = root / "docs/prompts/15-governance-lifecycle-contract.md"
    governance_prompt_text = governance_prompt_path.read_text(encoding="utf-8") if governance_prompt_path.exists() else ""
    checks.append(
        (
            "governance_subcontracts",
            all(
                token in governance_prompt_text
                for token in (
                    "Policy Sync Contract",
                    "Task Record Contract",
                    "Delta Check Contract",
                    "Human Confirmation Contract",
                    "Delegation Contract",
                    "治理控制面",
                )
            ),
            "governance contract includes the five governance subcontracts and task document control-plane guidance",
        )
    )
    checks.append(
        (
            "governance_no_stage_leak",
            "Stage 决定" not in governance_prompt_text,
            "governance contract no longer exposes stage language in the public default body",
        )
    )
    checks.append(
        (
            "runtime_not_in_default_paths",
            "纯 Skill / Copilot 路径" in docs_tasks_instruction_text
            and "额外状态文件" in docs_tasks_instruction_text,
            "public template keeps runtime concepts out of default docs instructions",
        )
    )

    scene_catalog_path = root / "docs/prompts/12-scene-catalog.md"
    scene_catalog_text = scene_catalog_path.read_text(encoding="utf-8") if scene_catalog_path.exists() else ""
    checks.append(
        (
            "scene_catalog_exists",
            scene_catalog_path.exists() and "Scene 1" in scene_catalog_text and "Scene 6" in scene_catalog_text,
            str(scene_catalog_path.relative_to(root)),
        )
    )

    method_catalog_path = root / "docs/prompts/13-method-catalog.md"
    method_catalog_text = method_catalog_path.read_text(encoding="utf-8") if method_catalog_path.exists() else ""
    checks.append(
        (
            "method_catalog_exists",
            method_catalog_path.exists() and "Method 1" in method_catalog_text,
            str(method_catalog_path.relative_to(root)),
        )
    )

    mode_catalog_path = root / "docs/prompts/14-mode-catalog.md"
    mode_catalog_text = mode_catalog_path.read_text(encoding="utf-8") if mode_catalog_path.exists() else ""
    checks.append(
        (
            "mode_catalog_exists",
            mode_catalog_path.exists() and "Strategy 1" in mode_catalog_text and "Strategy 3" in mode_catalog_text,
            str(mode_catalog_path.relative_to(root)),
        )
    )

    orchestrator_path = copilot_target_root / "prompts/wms-orchestrator.prompt.md"
    orchestrator_text = orchestrator_path.read_text(encoding="utf-8") if orchestrator_path.exists() else ""
    checks.append(
        (
            "copilot_orchestrator_guard",
            "15-governance-lifecycle-contract.md" in orchestrator_text
            and "12-scene-catalog.md" in orchestrator_text
            and "13-method-catalog.md" in orchestrator_text
            and "14-mode-catalog.md" in orchestrator_text
            and "16-governance-orchestrator.md" in orchestrator_text
            and "/wms-orchestrator" in repo_text
            and "DISCOVER / DELIVER / VERIFY" in orchestrator_text
            and "同一线程" in orchestrator_text
            and "一次性汇总" in orchestrator_text,
            "orchestrator prompt loads governance/scene/method/strategy catalogs and exposes the single default entry",
        )
    )
    orchestrator_source_path = root / "docs/prompts/16-governance-orchestrator.md"
    orchestrator_source_text = (
        orchestrator_source_path.read_text(encoding="utf-8") if orchestrator_source_path.exists() else ""
    )
    checks.append(
        (
            "orchestrator_control_plane",
            "当前控制文档" in orchestrator_source_text and "增量补充检查结果" in orchestrator_source_text,
            "orchestrator source prompt keeps the task document as the governance control plane",
        )
    )
    adapter_ref_path = root / "docs/skills-src/wms/governance-orchestrator/references/platform-confirmation-adapter.md"
    adapter_ref_text = adapter_ref_path.read_text(encoding="utf-8") if adapter_ref_path.exists() else ""
    delegation_ref_path = root / "docs/skills-src/wms/governance-orchestrator/references/delegation-payload.md"
    delegation_ref_text = delegation_ref_path.read_text(encoding="utf-8") if delegation_ref_path.exists() else ""
    checks.append(
        (
            "orchestrator_platform_adapter",
            "askQuestions" in adapter_ref_text and "显式发问" in adapter_ref_text and "默认继续检查文档" in adapter_ref_text,
            "platform confirmation adapter maps askQuestions and fallback behavior outside governance body",
        )
    )
    checks.append(
        (
            "orchestrator_delegation_payload",
            "Delegation Payload" in delegation_ref_text and "控制文档" in delegation_ref_text and "完成标准" in delegation_ref_text,
            "delegation payload reference exists for subagent inheritance",
        )
    )

    checks.append(
        (
            "copilot_no_legacy_default_prompts",
            not (copilot_target_root / "prompts/wms-scene-router.prompt.md").exists()
            and not (copilot_target_root / "prompts/wms-plan-gate.prompt.md").exists()
            and not (copilot_target_root / "prompts/wms-auto-dev.prompt.md").exists()
            and not (copilot_target_root / "prompts/wms-tdd.prompt.md").exists()
            and not (copilot_target_root / "prompts/wms-acd.prompt.md").exists()
            and not (copilot_target_root / "prompts/wms-aod.prompt.md").exists(),
            "legacy public default prompts were removed from generated Copilot assets",
        )
    )

    link_trace_path = copilot_target_root / "prompts/wms-link-trace.prompt.md"
    link_trace_text = link_trace_path.read_text(encoding="utf-8") if link_trace_path.exists() else ""
    checks.append(
        (
            "copilot_link_trace_guard",
            "15-governance-lifecycle-contract.md" in link_trace_text
            and "13-method-catalog.md" in link_trace_text
            and "08-link-confirmation.md" in link_trace_text
            and "/wms-link-trace" in repo_text,
            "link-trace prompt is generated as a method entry and anchored in repo instructions",
        )
    )

    evaluation_gate_path = copilot_target_root / "prompts/wms-evaluation-gate.prompt.md"
    evaluation_gate_text = evaluation_gate_path.read_text(encoding="utf-8") if evaluation_gate_path.exists() else ""
    checks.append(
        (
            "copilot_evaluation_gate_guard",
            "15-governance-lifecycle-contract.md" in evaluation_gate_text
            and "PASS / CONDITIONAL_PASS / BLOCKED / FAIL" in evaluation_gate_text
            and "不得写完成标记" in evaluation_gate_text,
            "evaluation-gate prompt enforces verdict and completion guard",
        )
    )

    checks.append(
        (
            "strategy_packs_stay_internal",
            "/wms-tdd" not in repo_text
            and "/wms-acd" not in repo_text
            and "/wms-aod" not in repo_text
            and "Strategy Packs" in repo_text,
            "strategy packs are described as internal orchestrator choices, not default slash prompts",
        )
    )

    all_prompt_texts = []
    for prompt_filename in expected_prompt_files:
        prompt_path = copilot_target_root / "prompts" / prompt_filename
        all_prompt_texts.append(prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else "")
    checks.append(
        (
            "copilot_all_prompts_inherit_lifecycle_contract",
            all(
                "15-governance-lifecycle-contract.md" in text
                and "规划任务" in text
                and "继续检查文档" in text
                for text in all_prompt_texts
            ),
            "all generated prompt files inherit the shared lifecycle contract",
        )
    )

    checks.append(("manual_fixture_count", len(fixture_metas) >= 9, f"fixtureCount={len(fixture_metas)}"))

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
