# 任务需求：task-modeling-v1

> English: [BRIEF.md](BRIEF.md)

**状态：** 已实现并通过本地验证
**研究目标：** G0，并为 G2–G4 提供支持

## 期望结果

为受控多步推理建立一个小型、确定性、可审计的任务校准 package。它必须表示任务侧
dependency structure，但不能声称该表示描述了 Transformer 内部计算。

第一版包含两个 pilot family：

1. symbolic function composition；
2. relational path composition。

选择它们是因为 chain length、presentation order、distractor、symbol vocabulary、
template 和 answer encoding 可以独立变化。任何 cross-family operation mapping 都必须
是可选、显式且标为 candidate hypothesis。

## 必需产物

1. 带版本的 task instance canonical record schema。
2. 两个 pilot family 的 deterministic generator 和 reference solver。
3. 明确的 instance dependency graph 和 generator trace。
4. 因子化 nuisance metadata 和稳定的 semantic instance identifier。
5. IID、held-out-surface、held-out-template 和 held-out-length split。
6. 由配置文件驱动的命令行数据生成入口。
7. 包含 configuration、seed、generator version、count、hash 和 split summary 的
   dataset manifest。
8. 提交到仓库的小型 fixture 和自动化测试。
9. 明确区分 generator trace 与模型 reasoning 的文档。

## 验收标准

1. 使用相同 configuration 和 seed 重复生成，得到逐字节相同的 canonical record 和
   相同 manifest hash。
2. 每个 target 都由不信任已存储答案的 reference solver 或 checker 验证。
3. 即使 prompt 不同，互斥 split 之间也不得存在重叠的 semantic instance identity。
4. 请求的 factor cell 和 split constraint 必须通过验证或明确失败；generator 不得
   静默生成不平衡的替代数据。
5. 小型 fixture 覆盖两个 task family 和全部 split type。
6. 测试覆盖 determinism、answer validity、schema validation、graph integrity、split
   leakage 和 CLI smoke behavior。
7. 在 Python 3.11 下，不使用 model weight 或网络即可完成本地 CPU smoke run。
8. 输出 manifest 记录足够 provenance，使 artifact 能从干净 checkout 中复现。

## 范围外

- 加载或查询 Transformer。
- 收集 chain of thought。
- 追踪 activation、attention、gradient 或 component。
- clustering、probe、functional fingerprint、ablation 或 patching。
- 声称某一 task family 或带标签 operation 是 universal。
- 大规模服务器生成或模型实验。
- 最终选择论文主任务。

## 已解决的审核问题

2026-09-08 批准：

1. 两个 pilot task family 都作为校准起点予以接受。
2. 中间状态保留为任务侧 annotation，默认永远不展示给模型。
3. Python 3.11 为项目基线。
