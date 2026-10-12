
# 用 Promptfoo 做评估

### 关于本评估套件的说明

1）请务必遵循下面的说明——尤其是关于所需依赖包的前置条件部分。

2）运行完整评估套件可能需要高于常规的速率限制。可以考虑在 Promptfoo 中只运行一部分测试。

3）并非每个测试都能开箱即用地通过——我们把评估设计为具有中等难度。

### 前置条件
要使用 Promptfoo，你需要在系统上安装 node.js 和 npm。更多信息请遵循[本指南](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

你可以用 npm 安装 promptfoo，也可以用 npx 直接运行。本指南中使用 npx。

*说明：在本示例中，你不需要运行 `npx promptfoo@latest init`，此目录下已经有一个初始化好的 `promptfooconfig.yaml` 文件*

官方文档见[这里](https://www.promptfoo.dev/docs/getting-started)

### 开始使用

开始使用前，请设置 ANTHROPIC_API_KEY 环境变量，或为你所选的提供方设置其他所需密钥。可以执行 `export ANTHROPIC_API_KEY=YOUR_API_KEY`。

然后 `cd` 进入 `evaluation` 目录，执行 `npx promptfoo@latest eval -c promptfooconfig.yaml --output ../data/results.csv`

之后，运行 `npx promptfoo@latest view` 即可查看结果。

### 工作原理

promptfooconfig.yaml 文件是我们评估设置的核心。它定义了几个关键部分：

提示词（Prompts）：
- 提示词从 prompts.py 文件导入。
- 这些提示词旨在检验语言模型表现的多个方面。

提供方（Providers）：
- 我们在这里配置所使用的 Claude 模型。

测试（Tests）：
- 测试用例在此定义。
- 这些测试指定了我们评估的输入与预期输出。
- Promptfoo 提供多种内置测试类型（见文档），你也可以自定义测试。

输出（Output）：
- 指定评估结果的格式与位置。
- Promptfoo 同样支持多种输出格式！

### 覆盖 Python 可执行文件

默认情况下，promptfoo 会在你的 shell 中运行 python。请确保 python 指向合适的可执行文件。

如果不存在 python 可执行文件，你会看到 "python: command not found" 错误。

要覆盖 Python 可执行文件，请设置 PROMPTFOO_PYTHON 环境变量。它可以是一个路径（例如 /path/to/python3.11），也可以是 PATH 中的一个可执行文件名（例如 python3.11）。