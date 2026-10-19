
# 用 Promptfoo 做评估

### 关于本评估套件的说明

1）请务必遵循下面的说明，尤其是关于所需包的前置条件。

2）运行完整评估套件可能需要高于常规的速率限制。考虑只在 promptfoo 中运行一部分测试。

3）并非每个测试都能开箱即用地通过——我们把评估设计成具有一定难度。

### 前置条件 
要使用 Promptfoo，你需要在系统上安装 node.js 和 npm。更多信息请遵循[这份指南](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)  

你可以用 npm 安装 promptfoo，也可以直接用 npx 运行。本指南使用 npx。

*说明：本示例不需要运行 `npx promptfoo@latest init`，本目录下已有初始化好的 `promptfooconfig.yaml` 文件*  

官方文档见[这里](https://www.promptfoo.dev/docs/getting-started)  

#### 注意 - 额外依赖
本示例需要安装以下依赖，custom_evals 才能正常运行。

`pip install nltk rouge-score`

### 开始使用

首先设置 ANTHROPIC_API_KEY 环境变量，或你所选提供方所需的其他密钥。可以执行 `export ANTHROPIC_API_KEY=YOUR_API_KEY`。

然后 `cd` 进入 `evaluation` 目录，并执行 `npx promptfoo@latest eval -c promptfooconfig.yaml --output ../data/results.csv`

之后，运行 `npx promptfoo@latest view` 即可查看结果。

### 工作原理

promptfooconfig.yaml 文件是我们评估配置的核心。它定义了若干关键部分：

提示词：
- 提示词从 prompts.py 文件导入。
- 这些提示词用于测试 LLM 表现的各个方面。


提供方：
- 我们在这里配置不同的 Claude 版本及其设置。
- 这让我们能够跨多个模型测试，或使用不同的参数（例如不同的温度设置）。


测试：
- 测试用例在本文件中定义，或如本例那样从 tests.yaml 导入。
- 这些测试指定评估的输入与预期输出。
- Promptfoo 提供多种内置测试类型（见文档），你也可以自定义。我们有 3 个自定义评估和 1 个开箱即用的评估（contains 方法）：
    - `bleu_eval.py`：实现 BLEU（Bilingual Evaluation Understudy）分数，用于衡量机器生成文本与参考文本之间的相似度。
    - `rouge_eval.py`：实现 ROUGE（Recall-Oriented Understudy for Gisting Evaluation）分数，通过与参考总结对比来评估总结的质量。
    - `llm_eval.py`：包含借助语言模型评估生成文本各方面表现的自定义评估指标，例如连贯性、相关性或事实准确性。

输出：
- 指定评估结果的格式和位置。
- Promptfoo 同样支持多种输出格式。

### 覆盖 Python 可执行文件

默认情况下，promptfoo 会在你的 shell 中运行 python。请确认 python 指向正确的可执行文件。

如果不存在 python 可执行文件，你会看到 “python: command not found” 错误。

要覆盖 Python 可执行文件，设置 PROMPTFOO_PYTHON 环境变量。可以设为一个路径（例如 /path/to/python3.11），或 PATH 中的一个可执行文件名（例如 python3.11）。