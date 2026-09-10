# 服务器环境：pilot-a0-target-grounding-v1

> English: [SERVER.md](SERVER.md)

**状态：** 不需要服务器；未授权网络、模型或服务器动作

## 当前任务

拟议 source inventory 是本地 metadata 与 documentation task，不需要 GPU、模型权重、
activation storage 或远程执行。

## Source access

实施审核必须另行说明：在线读取 official source metadata、下载到被忽略的本地 cache，还是
由用户提供。任何 download 都必须按 source 与 revision 得到明确、有边界的授权。

## 后续模型工作

Native behavioral inference、activation capture、MI/predictive analysis、cross-task transfer、
perturbation 与 intervention 是分别规划的未来任务。本方案有意不包含其 compute、model、
storage 与 server requirement。

