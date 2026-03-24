#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  create_task_dir.sh [--issue] [--owner "<name>"] [--branch "<branch>"] [--module "<module>"] [--link-trace] [--evaluation-gate] [--conversation-topic "<topic>"] "<task-name>"

Examples:
  create_task_dir.sh --owner "your-name" --module "example-service" "inventory-batch-fix"
  create_task_dir.sh --issue --owner "your-name" --module "example-service" --link-trace "outbound-status-mismatch"
EOF
}

mode="task"
owner="待填写"
branch="待填写"
module="待填写"
with_plan_gate=0
with_link_trace=0
with_evaluation_gate=0
conversation_topic=""
task_name=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --issue)
      mode="issue"
      shift
      ;;
    --owner)
      owner="${2:-}"
      shift 2
      ;;
    --branch)
      branch="${2:-}"
      shift 2
      ;;
    --module)
      module="${2:-}"
      shift 2
      ;;
    --plan-gate)
      with_plan_gate=1
      shift
      ;;
    --link-trace)
      with_link_trace=1
      shift
      ;;
    --evaluation-gate)
      with_evaluation_gate=1
      shift
      ;;
    --conversation-topic)
      conversation_topic="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -n "${task_name}" ]]; then
        printf 'Unexpected extra argument: %s\n' "$1" >&2
        usage
        exit 1
      fi
      task_name="$1"
      shift
      ;;
  esac
done

if [[ -z "${task_name}" ]]; then
  usage
  exit 1
fi

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
git_username="$(git -C "${repo_root}" config user.name 2>/dev/null || true)"
if [[ -z "${git_username}" ]]; then
  git_username="unknown"
fi
if [[ "${owner}" == "待填写" ]]; then
  owner="${git_username}"
fi
year="$(date +%Y)"
month="$(date +%m)"
today="$(date +%F)"
now_datetime="$(date '+%F %H:%M:%S')"

created_paths=()
verified_paths=()
readme_created=0

copy_if_missing() {
  local src="$1"
  local dst="$2"

  if [[ -f "${dst}" ]]; then
    verified_paths+=("${dst}")
    return
  fi

  cp "${src}" "${dst}"
  created_paths+=("${dst}")
  if [[ "${dst}" == */README.md ]]; then
    readme_created=1
  fi
}

render_placeholders() {
  local file_path="$1"
  local purpose="$2"

  FILE_PATH="${file_path}" \
  TASK_NAME="${task_name}" \
  OWNER="${owner}" \
  BRANCH="${branch}" \
  MODULE="${module}" \
  TODAY="${today}" \
  NOW_DATETIME="${now_datetime}" \
  PURPOSE="${purpose}" \
  CONVERSATION_FILE="01-${topic}.md" \
  python3 - <<'PY'
from pathlib import Path
import os

path = Path(os.environ["FILE_PATH"])
text = path.read_text(encoding="utf-8")

task_name = os.environ["TASK_NAME"]
owner = os.environ["OWNER"]
branch = os.environ["BRANCH"]
module = os.environ["MODULE"]
today = os.environ["TODAY"]
now_datetime = os.environ["NOW_DATETIME"]
purpose = os.environ["PURPOSE"]
conversation_file = os.environ["CONVERSATION_FILE"]

replacements = {
    "{简要描述}": task_name,
    "{一句话描述问题现象}": task_name,
    "{YYYY-MM-DD HH:mm}": now_datetime,
    "{YYYY-MM-DD}": today,
    "{日期}": today,
    "{姓名}": owner,
    "`feature/{分支名}`": f"`{branch}`",
    "feature/{分支名}": branch,
    "{分支名}": branch,
    "{example-service / example-deduction / ...}": module,
    "example-service / example-deduction / ...": module,
    "{关联任务名}": task_name,
    "{第N轮}": "第1轮",
    "{本次对话要解决什么问题}": purpose,
    "GitHub Copilot / Claude / ...": "Codex / Claude / Copilot",
    "[01-需求分析.md](ai-conversations/01-需求分析.md)": f"[{conversation_file}](ai-conversations/{conversation_file})",
    "[01-初步分析.md](ai-conversations/01-初步分析.md)": f"[{conversation_file}](ai-conversations/{conversation_file})",
}

for old, new in replacements.items():
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
PY
}

if [[ "${mode}" == "issue" ]]; then
  task_dir="${repo_root}/docs/tasks/${year}/${month}-[ISSUE]-${task_name}"
  readme_template="${repo_root}/docs/tasks/_templates/ISSUE_INVESTIGATION.md"
  default_topic="初步分析"
  default_purpose="问题初步分析、时间线整理与止血建议"
else
  task_dir="${repo_root}/docs/tasks/${year}/${month}-${task_name}"
  readme_template="${repo_root}/docs/tasks/_templates/TASK_RECORD.md"
  default_topic="任务启动"
  default_purpose="任务启动、目标澄清与上下文整理"
fi

topic="${conversation_topic:-${default_topic}}"
topic="${topic//\//-}"

mkdir -p "${task_dir}/ai-conversations" "${task_dir}/artifacts"

copy_if_missing "${readme_template}" "${task_dir}/README.md"
render_placeholders "${task_dir}/README.md" "${default_purpose}"
if [[ "${readme_created}" -eq 1 ]]; then
  python3 \
    "${repo_root}/docs/skills-src/wms/wms-task-governance/scripts/append_planning_marker.py" \
    "${task_dir}/README.md" \
    "${task_name}" \
    --iteration 1 \
    --user "${git_username}"
fi

copy_if_missing "${repo_root}/docs/tasks/_templates/BUSINESS_INSIGHT.md" "${task_dir}/business-insights.md"
render_placeholders "${task_dir}/business-insights.md" "${default_purpose}"

conversation_path="${task_dir}/ai-conversations/01-${topic}.md"
copy_if_missing "${repo_root}/docs/tasks/_templates/AI_CONVERSATION.md" "${conversation_path}"
render_placeholders "${conversation_path}" "${default_purpose}"

if [[ "${with_plan_gate}" -eq 1 ]]; then
  copy_if_missing \
    "${repo_root}/docs/skills-src/wms/plan-gate/assets/templates/plan-gate.md" \
    "${task_dir}/artifacts/plan-gate.md"
fi

if [[ "${with_link_trace}" -eq 1 ]]; then
  copy_if_missing \
    "${repo_root}/docs/skills-src/wms/link-trace-and-curation/assets/templates/link-trace.md" \
    "${task_dir}/artifacts/link-trace.md"
fi

if [[ "${with_evaluation_gate}" -eq 1 ]]; then
  copy_if_missing \
    "${repo_root}/docs/skills-src/wms/delivery-evaluation-gate/assets/templates/eval-plan.md" \
    "${task_dir}/artifacts/eval-plan.md"
  copy_if_missing \
    "${repo_root}/docs/skills-src/wms/delivery-evaluation-gate/assets/templates/eval-report.md" \
    "${task_dir}/artifacts/eval-report.md"
fi

printf 'Created or verified task directory: %s\n' "${task_dir}"
if [[ "${#created_paths[@]}" -gt 0 ]]; then
  printf 'Created files:\n'
  for path in "${created_paths[@]}"; do
    printf '  - %s\n' "${path#${repo_root}/}"
  done
fi
if [[ "${#verified_paths[@]}" -gt 0 ]]; then
  printf 'Verified existing files:\n'
  for path in "${verified_paths[@]}"; do
    printf '  - %s\n' "${path#${repo_root}/}"
  done
fi
