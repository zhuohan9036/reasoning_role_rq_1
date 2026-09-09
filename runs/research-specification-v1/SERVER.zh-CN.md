# 服务器环境：research-specification-v1

> English: [SERVER.md](SERVER.md)

**状态：** 不适用；未授权服务器执行

## 执行边界

这是一个仅修改文档的本地任务。规划以及后续可能获批的实施均不需要模型权重、网络、
GPU、scheduler、scratch storage 或服务器环境。

## 本地验证

- 验证所有计划修改的面向人类 Markdown 文件均具有同步的中英文版本和双向链接。
- 验证 `plan.json` 语法及其与人类可读方案的一致性。
- 检查修改路径 allowlist 和仓库状态。
- 检查术语，避免意外提出模型机制或因果结论。

## 禁止执行

- 不连接服务器或在服务器执行命令。
- 不下载 dependency 或模型。
- 不运行行为或机制实验。
- 不创建或检查 activation artifact。

任何后续模型或服务器任务仍需独立的动作预告、获批计划、精确 run 规格和服务器授权。

