# 服务器环境：pilot-a-design-v1

> English: [SERVER.md](SERVER.md)

**状态：** 未解决；未授权下载、模型、activation 或服务器执行

## 本地任务实施不需要的条件

Canonical task language、generator、solver、balance audit、split、paired rendering、
shortcut check 和本地 fixture 不需要 GPU、模型权重或网络访问。

## 行为执行前必须提供

- 所选 Mistral model 与 tokenizer 的 immutable full commit SHA。
- Instruction-tuned 或 base checkpoint 的确认。
- GPU 型号/数量、显存、CUDA、driver、PyTorch 和 Transformers 版本。
- Scheduler 或 launcher、wall-time、RAM 和存储限制。
- Model cache 与 generated-data path。
- 网络访问，或经过验证的预置本地权重。
- 经验证为 single-token 的 `Symbol8` rendering bank。
- 冻结的 behavior configuration 与 dataset manifest hash。

## 模型政策

- Pilot A 排除 Qwen。
- 工作默认：固定 immutable revision 的 `mistralai/Mistral-7B-Instruct-v0.3`。
- 首选替代：访问权限、许可条款和硬件允许时，使用相近规模的 Llama instruct checkpoint。
- 参数保持冻结并关闭 gradient。
- 在确定论文主要证据前重新审核模型选择；pilot checkpoint 不会自动升级为主模型。

## 相互独立的未来服务器 run

1. 只进行行为可行性运行，不保存 activation。
2. 只有行为审核与单独授权后，才进行 R1 residual-stream capture。
3. 只有冻结 discovery definition 后，才进行 untouched confirmation capture。
4. 可选 R2 或 semantic-domain replication；每项使用新的具名 run 合同。

每个 run 都必须有自己的准确 command、resource estimate、stopping condition、output
policy 和授权。大型输出保持在 Git 之外。

