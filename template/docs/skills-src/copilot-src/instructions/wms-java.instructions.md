---
applyTo: "example-*/src/main/java/**/*.java"
---

# WMS Java 路径指令

- 遵守 `Controller -> Service Impl -> Service Interface -> Datasource` 分层
- Web 层禁止直接访问 Mapper / DAO
- 新公共接口先在 `*-interface` 模块定义，再在 `*-service` 实现
- 保持 Query / Execute 分离，不要把读写职责混进同一个 Service
- 涉及公共符号、链路确认、影响面分析时，先走 `GitNexus > 局部 rg > 全项目搜索`
- 修改库存抵扣、串行处理、规则工厂前，先确认 `SkuSerialProcessor` 和规则分发影响
