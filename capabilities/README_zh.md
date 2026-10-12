# Claude 能力

欢迎来到 Claude Cookbooks 的能力（Capabilities）部分！本目录收录了一系列指南，展示 Claude 擅长的具体能力。每份指南都深入探讨某一项能力，讨论潜在使用场景、用于优化结果的提示词工程技巧，以及评估 Claude 表现的方法。

## 指南

- **[Classification with Claude](./classification/guide.ipynb)**：了解 Claude 如何革新分类任务，尤其是在业务规则复杂、训练数据有限的场景。本指南带你完成数据准备、结合检索增强生成（RAG）的提示词工程、测试和评估。

- **[Retrieval Augmented Generation with Claude](./retrieval_augmented_generation/guide.ipynb)**：学习如何用领域专业知识增强 Claude 的能力，即使用 RAG。本指南演示如何从零搭建 RAG 系统、优化其性能，并创建评估套件。你会了解摘要索引和重排序等技巧如何显著提升问答任务的精确率、召回率和整体准确率。

- **[Retrieval Augmented Generation with Contextual Embeddings](./contextual-embeddings/guide.ipynb)**：学习如何使用一项新技术提升 RAG 系统的性能。在传统 RAG 中，文档通常被切分为较小的片段以便高效检索。这种做法适用于许多应用，但当单个片段缺少足够上下文时会出问题。上下文嵌入向量（Contextual Embeddings）在嵌入之前为每个片段补充相关上下文，从而解决这一问题。你会了解如何把上下文嵌入向量与语义搜索、BM25 搜索和重排序结合使用以提升性能。

- **[Summarization with Claude](./summarization/guide.ipynb)**：探索 Claude 对多个来源的信息进行总结和综合的能力。本指南涵盖多种总结技巧，包括多示例、基于领域和分块的方法，以及处理长文档和多份文档的策略。我们也会探讨如何评估总结，这其中需要平衡艺术性、主观性和恰当的方法。

- **[Text-to-SQL with Claude](./text_to_sql/guide.ipynb)**：本指南介绍如何用提示词技巧、自我改进和 RAG，从自然语言生成复杂的 SQL 查询。我们还会探讨如何评估并提升生成 SQL 查询的准确性，其评估会测试语法、数据正确性、行数等内容。

- **[Knowledge Graph Construction with Claude](./knowledge_graph/guide.ipynb)**：端到端地从非结构化文本构建知识图谱——命名实体识别、关系抽取、实体消解和多跳查询——使用结构化输出完成经过模式校验的抽取，并用 Claude 驱动的去重取代字符串相似度启发式方法。

- **[Content Policy Enforcement with Claude](./content_moderation/guide.ipynb)**：把成文的内容政策转化为程序可执行的规则。Claude 将政策文字编译为经过校验的 JSON 规则，并从每条内容（文本和图像）中提取带类型的字段；确定性的规则引擎给出判定并保留完整的审计痕迹。涵盖广告创意、市场商品信息和社区内容。

## 开始使用

要使用这些指南，只需进入相应指南的目录，并按照 `guide.ipynb` 文件中的说明操作。每份指南都是自包含的，包含复现示例和实验所需的全部代码、数据和评估脚本。
