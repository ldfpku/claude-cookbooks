# 运维手册：OOMKilled / OutOfMemoryError

**症状：**容器以退出码 137 退出，pod 事件中显示 `OOMKilled`，应用日志中出现堆内存耗尽错误。

**分诊：**

1. 确认这次终止是 kubelet 的 OOM killer（退出码 137），而不是
   应用层面的限制。
2. 打开 `infra/k8s/<service>-deploy.yaml` 下的部署清单，
   检查 `spec.template.spec.containers[].resources.limits.memory`。
3. 如果该限制低于该服务已记录的工作集（checkout-svc
   在定价缓存预热后需要约 400Mi），就提高限制。512Mi 是标准的下一档。
4. 保持 `requests.memory` 不大于新的限制。

**修复：**在 infra 仓库上开一个 PR，提交修正后的限制。不要热修补线上部署。
