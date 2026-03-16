# Workflow

## 场景关注点

1. 层次归属：Controller / Interface / Service / Datasource
2. Query / Execute 分离是否正确
3. 是否已有可复用类、DTO、Mapper、Feign
4. 是否触发抵扣、MQ、事务或跨服务调用

## 建议顺序

1. 明确能力边界
2. 确认模块和调用链
3. 设计最小改动路径
4. 再进入实现、验证与评测门禁
