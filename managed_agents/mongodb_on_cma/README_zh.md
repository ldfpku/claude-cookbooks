# MongoDB on Claude Managed Agents

为 [**结合 MongoDB Atlas 与 Claude Managed Agents 的反欺诈审核智能体**](../CMA_with_mongodb_atlas.ipynb) cookbook 提供的安装样板代码。**教学代码内嵌在笔记本中**——四个检索管道构建器、自定义工具处理函数以及 `requires_action` 门控循环都在那里定义。本包只存放笔记本导入（而非阅读）的部分。

| 模块 | 内容 |
| --- | --- |
| [`config.py`](config.py) | 可调参数、索引名称，以及 MongoDB 服务器版本检查（`supports_rank_fusion`）。|
| [`embeddings.py`](embeddings.py) | 一个嵌入向量 + 重排序客户端，把 MongoDB Atlas AI 端点适配到 `voyageai` 接口，使该 cookbook 与提供方无关。|
| [`tools.py`](tools.py) | MongoDB Atlas 设置——填充集合、创建向量索引和 Atlas Search 索引并等待其可查询且完成同步、预检——此外还有笔记本的 `record_decision` 处理函数和 AP2 模块共用的决策/审计文档整形函数。|
| [`ap2_mandates.py`](ap2_mandates.py) | AP2（Agent Payments Protocol）授权的签名与验证（ES256 JWT）——一个加密黑盒，笔记本通过 `verify_mandates` 调用它并根据其判定结果行动。|
| [`seed.py`](seed.py) | 从 [`../example_data/mongodb_on_cma/`](../example_data/mongodb_on_cma/seed_transactions.jsonl) 加载明文测试数据。|
| [`self_hosted_sandbox/`](self_hosted_sandbox/) | 该 cookbook 路径 B 所用的 Docker 镜像：一个内置 `pymongo` 的自托管沙箱，智能体从 `bash` 中查询 MongoDB，`MONGO_URI` 只是一个普通的容器环境变量。它不是 Python 模块，也没有任何代码导入它。|

MongoDB 凭据（`MONGO_URI`）始终只存在于边界你这一侧：`pymongo` 运行在笔记本宿主侧的处理函数中，绝不出现在智能体上下文或其沙箱里。连接模式以及端到端的反欺诈审核智能体请参阅该 cookbook。
