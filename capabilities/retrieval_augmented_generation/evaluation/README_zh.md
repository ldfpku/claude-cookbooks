# 用 Promptfoo 进行评估

### 前置条件
使用 Promptfoo 需要在系统中安装 node.js 和 npm。更多信息请遵循[这份指南](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

你可以用 npm 安装 promptfoo，也可以直接用 npx 运行。本指南使用 npx。

*说明：本示例无需运行 `npx promptfoo@latest init`，该目录下已有初始化好的 `promptfooconfig.yaml` 文件*

官方文档见[这里](https://www.promptfoo.dev/docs/getting-started)


### 开始使用
评估由 `promptfooconfig...` 这些 `.yaml` 文件编排。在我们的应用中，评估逻辑分为两部分：`promptfooconfig_retrieval.yaml` 用于评估检索系统，`promptfooconfig_end_to_end.yaml` 用于评估端到端表现。在每个文件中我们定义如下部分

### 检索评估

- 提示词
    - Promptfoo 支持以多种不同格式导入提示词。详情可阅读[这里](https://www.promptfoo.dev/docs/configuration/parameters)。
    - 在我们的场景中，每次不必重新编写提示词，只需把 `{{query}}` 直接传递给每个检索“提供方”进行评估
- 提供方
    - 我们没有使用标准的 LLM 提供方，而是为 `guide.ipynb` 中的每种检索方法编写了自定义提供方
- 测试
    - 我们使用与 `guide.ipynb` 相同的数据。把它拆分为 `end_to_end_dataset.csv` 和 `retrieval_dataset.csv`，并在每个数据集中增加 `__expected` 列，从而可以对每一行自动执行断言
    - 检索评估逻辑可在 `eval_end_to_end.py` 中找到

### 端到端评估

- 提示词
    - Promptfoo 支持以多种不同格式导入提示词。详情可阅读[这里](https://www.promptfoo.dev/docs/configuration/parameters)。
    - 我们的端到端评估配置中有 3 条提示词：每条对应一种使用方法
        - 这些函数与 `guide.ipynb` 中使用的完全相同，区别在于它们不调用 Claude API，而是直接返回提示词。Promptfoo 负责编排 API 调用并保存结果。
        - 关于提示词函数可阅读[这里](https://www.promptfoo.dev/docs/configuration/parameters#prompt-functions)。使用 Python 让我们能够复用 VectorDB 类，这是 RAG 所必需的，该类定义在 `vectordb.py` 中。
- 提供方
    - 通过 Promptfoo 可以连接来自不同平台的多种 LLM，详见[这里](https://www.promptfoo.dev/docs/providers)。在 `guide.ipynb` 中我们使用 Haiku，温度默认 0.0。我们将用 Promptfoo 尝试不同模型。
- 测试
    - 我们使用与 `guide.ipynb` 相同的数据。把它拆分为 `end_to_end_dataset.csv` 和 `retrieval_dataset.csv`，并在每个数据集中增加 `__expected` 列，从而可以对每一行自动执行断言
    - Promptfoo 提供丰富的内置测试，清单见[这里](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic)。
    - 检索系统的测试逻辑在 `eval_retrieval.py` 中，端到端系统的测试逻辑在 `eval_end_to_end.py` 中
- 输出
    - 我们定义输出文件的路径。Promptfoo 支持多种输出格式，[见这里](https://www.promptfoo.dev/docs/configuration/parameters/#output-file)。你也可以使用 Promptfoo 的网页界面，[见这里](https://www.promptfoo.dev/docs/usage/web-ui)。


### 运行评估

要开始使用 Promptfoo，请打开终端并进入本目录（`./evaluation`）。

在运行评估之前，必须定义以下环境变量：

`export ANTHROPIC_API_KEY=YOUR_API_KEY`  
`export VOYAGE_API_KEY=YOUR_API_KEY`

在 `evaluation` 目录下，运行下列命令之一。

- 评估端到端系统表现：`npx promptfoo@latest eval -c promptfooconfig_end_to_end.yaml --output ../data/end_to_end_results.json`

- 单独评估检索系统表现：`npx promptfoo@latest eval -c promptfooconfig_retrieval.yaml --output ../data/retrieval_results.json`

评估完成后，终端会打印数据集每一行的结果。你也可以运行 `npx promptfoo@latest view`，在 promptfoo 界面查看器中查看输出。