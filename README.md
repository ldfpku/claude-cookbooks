# Claude Cookbooks

The Claude Cookbooks provide code and guides designed to help developers build with Claude, offering copy-able code snippets that you can easily integrate into your own projects.

## Prerequisites

Most examples that use the Anthropic Messages API can run against the Anthropic-compatible
[Qwen gateway](https://qwen.smjtools.com). Examples that depend on Claude-only APIs or services
still require an Anthropic API key.

### Use the Qwen gateway for cookbook examples

The gateway serves the Qwen3.8-Flash-Next model and accepts Anthropic Messages API requests. Create
a cookbook-specific environment file and enter your personal gateway key:

```bash
cp .cookbook.env.example .cookbook.env
# Edit .cookbook.env and replace YOUR_QWEN_GATEWAY_KEY with your personal gateway key.
```

If `.cookbook.env` already exists, edit it without replacing it with the template.

For a local Python 3.15 environment, update dependencies and pin the interpreter:

```powershell
uv python pin 3.15
uv sync --python 3.15 --all-extras --upgrade
uv run python -m ipykernel install --sys-prefix --name cookbook-venv --display-name "Python 3.15 (cookbook .venv)"
```

The project retains Python 3.11 as its minimum; the local `.python-version` pin is not
committed. VoyageAI currently declares Python `<3.15` and is installed only on those
versions. Run VoyageAI examples in a separate compatible environment.
On Windows, building `pywinpty` from source requires NuGet. Its source-built wheel may
omit `conpty.dll` and `OpenConsole.exe`; verify `import winpty` before starting Jupyter
and install the matching Microsoft-signed ConPTY runtime into the environment's
`Lib\site-packages\winpty` directory if needed. Recreating the environment requires
checking these native runtime files again.

Start Jupyter with that file so its kernels inherit the gateway settings:

```bash
uv run --env-file .cookbook.env python -m jupyterlab
```

This runs JupyterLab as a Python module, avoiding Windows console-launcher errors such as
`uv trampoline failed to canonicalize script path`.

For a Python example, use the same project-scoped settings:

```bash
uv run --env-file .cookbook.env python path/to/example.py
```

These commands pass settings only to the launched process and its child processes; they do not
change system or user environment variables or the configuration of Claude Desktop or Claude Code.
Keep `.cookbook.env` private. The existing `.env` and `.env.example` remain separate and are not
overwritten by this setup.

The gateway documents `POST /v1/messages` compatibility, not full Claude API parity. Claude Agent
SDK examples and examples requiring other Anthropic endpoints (such as Batch, Files, or Admin API)
must use Anthropic API credentials and the Anthropic endpoint. Messages-level features beyond the
documented compatibility should be checked against the gateway's current support. Long requests
should use streaming, as the gateway may time out non-streaming requests that take too long;
image requests require an available vision-enabled node.

### Use the Anthropic API

For examples that require Claude-only APIs or services, get an Anthropic API key from
[Anthropic Console](https://console.anthropic.com/settings/keys) and configure it separately. Do
not use your gateway key for those examples. The repository's `.env.example` remains the
Anthropic-key template; if you need a local `.env`, create it only when one does not already exist.
Run those examples in a separate process without the cookbook gateway environment, for example:

```bash
uv run --env-file .env python -m jupyterlab
```

While the code examples are primarily written in Python, the concepts can be adapted to any programming language that supports interaction with the Claude API.

If you're new to working with the Claude API, we recommend starting with our [Claude API Fundamentals course](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals) to get a solid foundation.

## Explore Further

Looking for more resources to enhance your experience with Claude and AI assistants? Check out these helpful links:

- [Anthropic developer documentation](https://docs.claude.com/claude/docs/guide-to-anthropics-prompt-engineering-resources)
- [Anthropic support docs](https://support.anthropic.com)
- [Anthropic Discord community](https://www.anthropic.com/discord)

## Contributing

The Claude Cookbooks thrives on the contributions of the developer community. We value your input, whether it's submitting an idea, fixing a typo, adding a new guide, or improving an existing one. By contributing, you help make this resource even more valuable for everyone.

To avoid duplication of efforts, please review the existing issues and pull requests before contributing.

If you have ideas for new examples or guides, share them on the [issues page](https://github.com/anthropics/anthropic-cookbook/issues).

## Table of recipes

### Capabilities
- [Classification](https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/classification): Explore techniques for text and data classification using Claude.
- [Retrieval Augmented Generation](https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/retrieval_augmented_generation): Learn how to enhance Claude's responses with external knowledge.
- [Summarization](https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/summarization): Discover techniques for effective text summarization with Claude.

### Tool Use and Integration
- [Tool use](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use): Learn how to integrate Claude with external tools and functions to extend its capabilities.
  - [Customer service agent](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/customer_service_agent.ipynb)
  - [Calculator integration](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/calculator_tool.ipynb)
  - [SQL queries](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/how_to_make_sql_queries.ipynb)

### Third-Party Integrations
- [Retrieval augmented generation](https://github.com/anthropics/anthropic-cookbook/tree/main/third_party): Supplement Claude's knowledge with external data sources.
  - [Vector databases (Pinecone)](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Pinecone/rag_using_pinecone.ipynb)
  - [Wikipedia](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Wikipedia/wikipedia-search-cookbook.ipynb/)
  - [Web pages](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/read_web_pages_with_haiku.ipynb)
- [Embeddings with Voyage AI](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/VoyageAI/how_to_create_embeddings.md)

### Multimodal Capabilities
- [Vision with Claude](https://github.com/anthropics/anthropic-cookbook/tree/main/multimodal): 
  - [Getting started with images](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/getting_started_with_vision.ipynb)
  - [Best practices for vision](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/best_practices_for_vision.ipynb)
  - [Interpreting charts and graphs](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/reading_charts_graphs_powerpoints.ipynb)
  - [Extracting content from forms](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/how_to_transcribe_text.ipynb)
- [Generate images with Claude](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/illustrated_responses.ipynb): Use Claude with Stable Diffusion for image generation.

### Advanced Techniques
- [Sub-agents](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/using_sub_agents.ipynb): Learn how to use Haiku as a sub-agent in combination with Opus.
- [Upload PDFs to Claude](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/pdf_upload_summarization.ipynb): Parse and pass PDFs as text to Claude.
- [Automated evaluations](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/building_evals.ipynb): Use Claude to automate the prompt evaluation process.
- [Enable JSON mode](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/how_to_enable_json_mode.ipynb): Ensure consistent JSON output from Claude.
- [Create a moderation filter](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/building_moderation_filter.ipynb): Use Claude to create a content moderation filter for your application.
- [Prompt caching](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/prompt_caching.ipynb): Learn techniques for efficient prompt caching with Claude.
- [Cost optimization](https://github.com/anthropics/anthropic-cookbook/blob/main/cost_optimization/cost_optimization.ipynb): Work through a cost optimization checklist on an agent, measuring pass rate and cost per task to find the Pareto-optimal configuration.

## Additional Resources

- [Anthropic on AWS](https://github.com/aws-samples/anthropic-on-aws): Explore examples and solutions for using Claude on AWS infrastructure.
- [AWS Samples](https://github.com/aws-samples/): A collection of code samples from AWS which can be adapted for use with Claude. Note that some samples may require modification to work optimally with Claude.
