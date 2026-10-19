# 用 Promptfoo 做评估



### 前置条件 
要使用 Promptfoo，你需要在系统上安装 node.js 和 npm。更多信息请遵循[这份指南](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)  

你可以用 npm 安装 promptfoo，也可以直接用 npx 运行。本指南使用 npx。

*说明：本示例不需要运行 `npx promptfoo@latest init`，本目录下已有初始化好的 `promptfooconfig.yaml` 文件*  

官方文档见[这里](https://www.promptfoo.dev/docs/getting-started)  



### 开始使用
评估由 `promptfooconfig.yaml` 文件编排。该文件中定义以下部分：

- 提示词
    - Promptfoo 支持以多种格式导入提示词。更多信息见[这里](https://www.promptfoo.dev/docs/configuration/parameters)。
    - 本示例加载 3 个提示词——即 `guide.ipynb` 中用到的同一组提示词，从 `prompts.py` 文件读取：
        - 这些函数与 `guide.ipynb` 中的完全相同，只是不调用 Claude API，而仅返回提示词。随后由 Promptfoo 负责编排 API 调用并保存结果。
        - 关于提示词函数的更多信息见[这里](https://www.promptfoo.dev/docs/configuration/parameters#prompt-functions)。使用 Python 让我们可以复用 RAG 所必需的 VectorDB 类，该类定义在 `vectordb.py` 中。
- 提供方
    - 通过 Promptfoo 可以连接来自不同平台的多种 LLM，详见[这里](https://www.promptfoo.dev/docs/providers)。在 `guide.ipynb` 中我们使用 Haiku，温度默认 0.0。我们将用 Promptfoo 试验一组不同的温度设置，以找出适合我们场景的最优选择。
- 测试
    - 我们使用 `guide.ipynb` 中相同的数据，见 [`dataset.csv`](./dataset.csv)。
    - Promptfoo 内置了丰富的测试，见[这里](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic)。
    - 本示例在 `dataset.csv` 中定义测试，因为评估条件随每一行变化；并在 `promptfooconfig.yaml` 中定义测试，用于所有测试用例中保持一致的条件。更多信息见[这里](https://www.promptfoo.dev/docs/configuration/parameters/#import-from-csv)
- 转换
    - 在 `defaultTest` 部分我们定义一个转换函数。这是一个 Python 函数，从 LLM 响应中提取我们要测试的特定输出。
- 输出
    - 我们定义输出文件的路径。Promptfoo 可以以多种格式输出结果，[见这里](https://www.promptfoo.dev/docs/configuration/parameters/#output-file)。你也可以使用 Promptfoo 的网页界面，[见这里](https://www.promptfoo.dev/docs/usage/web-ui)。


### 运行评估

要开始使用 Promptfoo，请打开终端并进入本目录（`./evaluation`）。

运行评估之前，必须定义以下环境变量：

`export ANTHROPIC_API_KEY=YOUR_API_KEY`  
`export VOYAGE_API_KEY=YOUR_API_KEY`

在 `evaluation` 目录下，运行以下命令。

`npx promptfoo@latest eval`

如果你想提高请求的并发度（默认 = 4），运行以下命令。

`npx promptfoo@latest eval -j 25`  

评估完成后，终端会为数据集中的每一行打印结果。

现在可以回到 `guide.ipynb` 分析结果！


