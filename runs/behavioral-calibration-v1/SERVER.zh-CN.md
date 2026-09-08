# 服务器环境：behavioral-calibration-v1

> English: [SERVER.md](SERVER.md)

**状态：** 尚未解决；未授权服务器执行

## 真实模型运行前的必需信息

- Exact model 和 tokenizer ID，以及 immutable revision。
- Base checkpoint 或 instruction-tuned checkpoint。
- Plain prompt 或固定的 tokenizer chat template。
- GPU 型号/数量、VRAM、CUDA、driver 和支持的 PyTorch version。
- Launcher 或 scheduler、wall time、CPU、RAM 和 storage limit。
- Model cache、dataset、scratch output 和 compact result path。
- 使用 Internet 下载，还是使用预先准备的 local-only weight。
- 获批的 dependency lock 或现有 server environment。

## 模型选择约束

Pilot model 应提供冻结且固定版本的 weight，通过可检查的本地代码加载，为后续独立任务
暴露 internal tensor；除非经过审核，应避免 `trust_remote_code`；模型需适配获批 GPU，
并且在没有 task-specific training 的情况下达到足够表现。后续 replication model 应在
model family 或 architecture 上具有实质差异。

## 本地验证

- Python 3.11，不使用网络或模型下载。
- 使用 fake backend 验证 output、failure、resume 和 summary。
- 以轻量 stub 检查 freeze/no-gradient adapter contract。
- 可选模型依赖与 task-data package 隔离。

## 提议的服务器顺序

执行仍处于阻塞状态，必须明确授权后才能开始：

1. 记录环境并验证固定版本的本地 model file；
2. 运行测试和一个 batch 的 model-load check；
3. 人工检查 8–16 个平衡 sample；
4. 冻结 pilot configuration 及其 hash；
5. 开启 resume 并运行完整 pilot；
6. 重放一个 deterministic subset；
7. 生成 metric、interval、runtime、memory 和 failure diagnostic；
8. 只把小型 artifact 返回 Git。

本任务不允许保存 activation dump。
