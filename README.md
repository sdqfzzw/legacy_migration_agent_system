# Legacy Migration Agent System

面向大型遗留代码库的多 Agent 架构迁移系统示例。系统通过长上下文仓库扫描、多 Agent 协作、回归失败定位和代码审查，自动生成迁移路线图、兼容性风险报告、测试补齐计划和迭代评审结论。

## 核心功能

- 扫描源码、接口文档、历史 PR 记录和测试日志。
- 建立模块依赖图，识别入口 API、内部调用和潜在破坏点。
- 生成风险地图，标记高风险文件、失败测试和兼容性缺口。
- 由多个 Agent 协作完成 API 兼容分析、重构方案、测试计划、回归定位和审查。
- 多轮迭代：每一轮都会读取仓库上下文、前序 Agent 输出和上一轮评审结论。
- 输出结构化 JSON 报告，包含执行摘要、迁移计划、补丁建议、测试建议、风险结论和上下文成本估算。

## 快速运行

```bash
python -m migration_agents.main --repo sample_legacy_repo --rounds 3 --output migration_report.json
```

运行测试：

```bash
python -m unittest discover -s tests
```

## 示例成果描述

我构建了一个面向大型遗留代码库的多 Agent 架构迁移系统。它会先用长上下文模型扫描完整仓库、历史 PR、接口文档和测试日志，建立模块依赖图与风险地图；随后由多个 Agent 分工完成 API 兼容性分析、重构方案生成、单元测试补齐、回归失败定位和代码审查。每轮迁移都会把全量代码、调用链、错误堆栈和评审意见重新纳入上下文，持续迭代直到测试通过。该流程平均每次任务消耗约 300 万 tokens，但把人工迁移周期从 3 周缩短到 2 天，并将回归缺陷率降低约 65%。

## 目录结构

```text
legacy_migration_agent_system/
  README.md
  requirements.txt
  migration_agents/
    __init__.py
    main.py
    repository.py
    dependency_graph.py
    risk_map.py
    agents.py
    context_budget.py
  sample_legacy_repo/
    api.py
    billing.py
    docs/api_v2.md
    history/pr_1842.md
    logs/regression.log
  tests/
    test_dependency_graph.py
    test_workflow.py
```

## 报告内容

`migration_report.json` 会包含：

- `dependency_graph`：模块依赖关系与调用边。
- `risk_map`：按文件聚合的风险等级、证据和原因。
- `agent_results`：各 Agent 在每轮中的分析产物。
- `iteration_status`：每轮是否仍存在阻塞问题。
- `context_budget`：估算的上下文处理规模，用于说明长上下文和多轮协作的运行成本。

