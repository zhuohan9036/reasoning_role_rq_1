# 服务器环境：task-modeling-v1

> English: [SERVER.md](SERVER.md)

**状态：** 信息不完整；未授权服务器执行

## 已知约束

- 操作系统：Ubuntu。
- 首选 Python 基线：3.11，等待确认。
- 正式模型训练和大型机制实验只能在服务器运行。
- 本任务所需的验收运行只使用 CPU，应能在本地完成。

## 未知环境字段

- Host/access method。
- Scheduler 或 job launcher。
- GPU 型号与数量。
- NVIDIA driver 和 CUDA 版本。
- 可用 CPU、RAM 和本地 scratch storage。
- 共享 dataset、model cache 和 result path。
- Internet/registry access policy。
- Environment manager 与获准的 dependency installation process。
- Job time limit 与 preemption behavior。
- Artifact transfer 与 backup policy。

## 验证划分

### 任务验收前必须在本地完成

- 在干净 Python 3.11 环境安装 package。
- 执行实现阶段选定的 formatting/static check。
- 执行完整 unit 和 integration test suite。
- 生成两次可提交规模的 smoke dataset 并比较 hash。

### 延后的服务器验证

- 根据提交的 metadata 重建环境。
- 在 server scratch storage 中生成更大的 calibration dataset。
- Artifact 传输后验证 manifest 和 hash。
- 测量 runtime、peak RAM 和 storage footprint。
- 确认 artifact 中不存在本地绝对路径。

本任务不使用模型，因此有意延后 GPU/CUDA 验证。服务器命令必须等 O-009 解决后才能
编写，且未经明确授权不得执行。
