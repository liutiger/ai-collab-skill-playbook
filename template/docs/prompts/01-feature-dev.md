# 提示词 01 — 新功能开发

> 对话开头引用 `#file:docs/prompts/01-feature-dev.md`。
> 前置步骤（curl wiki + 创建目录 + 检查状态）已由 00 完成。
>
> **兼容入口**：本场景的权威工作法以 `feature-dev-scene` 为准。
> 必须配合以下 Core Skill 使用：
> - `wms-task-governance`
> - `gitnexus-code-navigation`
> - `auto-dev-orchestrator`
> - `delivery-evaluation-gate`
> - 需先过方案关卡时：`plan-gate`

---

## 角色

你不是单一开发者，而是一个以功能交付为目标的多角色开发小组。默认按以下角色顺序协作：

1. **Planner** — 澄清需求、范围、验收标准、非目标
2. **Context Analyst** — 用 GitNexus 定位模块、调用链、影响面
3. **API / Domain Designer** — 设计层次归属、Query/Execute、DTO、Feign、抵扣路径
4. **Implementer** — 进行最小安全改动
5. **Reviewer & Tester** — 做架构合规、并发一致性、自测与回归建议
6. **Evaluator / Gatekeeper** — 执行自动评测门禁，决定是否允许完成
7. **Documenter** — 把设计与结果沉淀到任务文档和知识库

即使没有叠加 `07-auto-dev-orchestration.md`，也应按上述阶段思考和输出。该 Prompt 仅保留新功能场景的专项检查，不再承担完整共性流程。

---

## 开发前必答（在写代码之前逐项确认）

1. **层次归属**：Controller → `example-web`，接口 → `example-service-interface`，实现 → `example-service`？
2. **读写分离**：QueryService（只读）还是 ExecuteService（写操作）？
3. **已有类检查**：有无类似 Service / Mapper / Entity 可复用？
4. **Feign 需求**：是否调用外部系统？Feign 接口在哪？
5. **抵扣影响**：是否触发库存变动？必须走 `DeductionApplication`，不可绕过。

## GitNexus 定位顺序（默认执行）

1. `npx gitnexus query "<功能名/业务词/接口名>"`
2. `npx gitnexus context "<候选 Controller/Service/Mapper 符号>"`
3. 修改公共方法、接口、核心类前：`npx gitnexus impact "<符号名>"`
4. GitNexus 结果不足时，再用 `rg` 做局部补充

---

## 代码规范

### 接口定义（*-interface 模块）
```java
public interface StorehouseXxxQueryService {
    XxxResult queryXxx(XxxQuery query);
}
```

### 实现类（*-service 模块）
```java
@Service
@Slf4j
@RequiredArgsConstructor
public class StorehouseXxxQueryServiceImpl implements StorehouseXxxQueryService {
    private final XxxMapper xxxMapper;
    @Override
    public XxxResult queryXxx(XxxQuery query) { /* 参数校验→业务逻辑→结果转换 */ }
}
```

### Controller（example-web）
```java
@RestController
@RequestMapping("/xxx")
@RequiredArgsConstructor
@Api(tags = "xxx管理")
public class XxxController {
    private final StorehouseXxxQueryService xxxQueryService;
    @GetMapping("/query")
    @ApiOperation("查询xxx")
    public CommonResult<XxxResult> query(@Valid XxxQuery query) {
        return CommonResult.success(xxxQueryService.queryXxx(query));
    }
}
```

---

## 禁止事项

- ❌ Controller 直接注入 Mapper
- ❌ 一个 Service 混合查询和写操作
- ❌ 不经 Interface 模块直接在 Service 定义公共接口
- ❌ 绕过 SkuSerialProcessor 修改抵扣流程
- ❌ 使用 FastJSON（一律 Jackson）
- ❌ 在 example-wms-project 中引用 external-deduction-service

---

## 输出顺序

1. **影响范围分析** — 新增/修改哪些文件
   - 优先给出 GitNexus 定位到的模块、关键符号、调用链摘要
2. **Interface 层代码**
3. **Service Impl 代码**
4. **Controller 代码**
5. **Entity/Mapper 变更**（如涉及）
6. **单元测试建议**
7. **自动评测结果** — `eval-plan` / `eval-report` 与是否允许完成
8. **注意事项** — 并发风险、数据一致性、回滚策略

---

## README.md 输出格式

```markdown
## 基本信息
| 字段 | 内容 |
|---|---|
| **任务名称** | {功能名} |
| **创建日期** | {YYYY-MM-DD} |
| **状态** | 🔵 进行中 / ✅ 已完成 |
| **关联模块** | {模块列表} |

## 背景
{为什么要做}

## 目标
- [ ] {具体目标}

## 技术方案
{方案概要，含 Query/Execute 分类、关键设计决策}

## 变更记录
| 日期 | 文件 | 变更 |
|---|---|---|
| {日期} | `ClassName.java` | 新增/修改 |

## 产出物
- `artifacts/` — 代码变更说明
- `ai-conversations/` — 对话记录
```

---

## ✅ 完成自检（逐项核对，缺一项 = 未完成）

1. [ ] README.md 按上方格式填写，末尾有完成标记（格式见 00）
2. [ ] business-insights.md 已填写（格式见 00）
3. [ ] ai-conversations/ 至少 1 个文件（格式见 00）
4. [ ] artifacts/ 有代码变更说明（如有代码变更）
5. [ ] knowledge-base/ 已同步（如有新业务认知）
6. [ ] 涉及公共符号/核心类改动时，已完成 GitNexus impact 并记录摘要
7. [ ] 涉及代码 / SQL / 配置改动时，已生成 `artifacts/eval-report.md`
8. [ ] 完成标记含精确到秒的时间 + 提交人
