#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  run_maven_eval_gate.sh --modules "example-service,example-web" --report "/abs/path/eval-report.md" [--spotbugs]

Examples:
  run_maven_eval_gate.sh --modules "example-service" --report "docs/tasks/2026/03-demo/artifacts/eval-report.md"
  run_maven_eval_gate.sh --modules "example-service,example-web" --report "docs/tasks/2026/03-demo/artifacts/eval-report.md" --spotbugs
EOF
}

modules=""
report_path=""
run_spotbugs=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --modules)
      modules="${2:-}"
      shift 2
      ;;
    --report)
      report_path="${2:-}"
      shift 2
      ;;
    --spotbugs)
      run_spotbugs=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unexpected argument: %s\n' "$1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${modules}" || -z "${report_path}" ]]; then
  usage
  exit 1
fi

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
report_abs="${report_path}"
if [[ "${report_abs}" != /* ]]; then
  report_abs="${repo_root}/${report_abs}"
fi

report_dir="$(dirname "${report_abs}")"
log_dir="${report_dir}/eval-logs"
mkdir -p "${report_dir}" "${log_dir}"

overall="PASS"
rows=()

run_gate() {
  local gate_name="$1"
  local gate_slug="$2"
  shift 2

  local log_file="${log_dir}/${gate_slug}.log"
  local cmd_display
  printf -v cmd_display '%q ' "$@"
  cmd_display="${cmd_display% }"

  if (
    cd "${repo_root}"
    "$@"
  ) >"${log_file}" 2>&1; then
    local status="PASS"
  else
    local status="FAIL"
    overall="FAIL"
  fi

  rows+=("| ${gate_name} | \`${cmd_display}\` | ${status} | \`${log_file#${repo_root}/}\` |")
}

compile_cmd=(mvn -pl "${modules}" -am -DskipTests compile)
test_cmd=(mvn -pl "${modules}" -am test)

run_gate "编译门禁" "01-compile" "${compile_cmd[@]}"
run_gate "测试门禁" "02-test" "${test_cmd[@]}"

if [[ "${run_spotbugs}" -eq 1 ]]; then
  spotbugs_cmd=(mvn -pl "${modules}" -am -DskipTests spotbugs:spotbugs)
  run_gate "静态门禁" "03-spotbugs" "${spotbugs_cmd[@]}"
else
  rows+=("| 静态门禁 | `未执行` | SKIPPED | `未启用 --spotbugs` |")
fi

completion_allowed="是"
next_action="可进入文档沉淀和完成判断"
if [[ "${overall}" == "FAIL" ]]; then
  completion_allowed="否"
  next_action="先修复失败门禁，再重新执行评测"
fi

cat >"${report_abs}" <<EOF
## 评测结果
| 门禁 | 命令 | 状态 | 证据 / 日志 |
|---|---|---|---|
$(printf '%s\n' "${rows[@]}")

## 评测结论
- 总体结论：${overall}
- 是否允许写完成标记：${completion_allowed}
- 残留风险：
- 下一步动作：${next_action}
EOF

printf 'Evaluation report written to: %s\n' "${report_abs}"

if [[ "${overall}" == "FAIL" ]]; then
  exit 1
fi
