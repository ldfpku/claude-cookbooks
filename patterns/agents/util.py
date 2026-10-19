import os
import re

from anthropic import Anthropic

# client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

gateway_url = os.environ.get("ANTHROPIC_BASE_URL", "").rstrip("/")
gateway_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

if gateway_url != "https://qwen.smjtools.com":
    raise RuntimeError("当前内核没有 cookbook 网关配置。")
if not gateway_key or gateway_key == "YOUR_QWEN_GATEWAY_KEY":
    raise RuntimeError("请配置个人网关密钥并重启 Jupyter。")
if gateway_key.startswith("sk-ant-"):
    raise RuntimeError("不要将 Anthropic 密钥发送到 Qwen 网关。")
if os.environ.get("ANTHROPIC_AUTH_TOKEN"):
    raise RuntimeError("存在额外 auth token，请使用独立启动环境。")

client = Anthropic(
    api_key=gateway_key,
    base_url=gateway_url,
    timeout=180.0,
    max_retries=0,
)
MODEL_NAME = "strata"


def llm_call(prompt: str, system_prompt: str = "", model="claude-sonnet-4-6") -> str:
    """
    Calls the model with the given prompt and returns the response.

    Args:
        prompt (str): The user prompt to send to the model.
        system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
        model (str, optional): The model to use for the call. Defaults to "claude-sonnet-4-6".

    Returns:
        str: The response from the language model.
    """
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=messages,
        # temperature=0.1,
    )
    return response.content[0].text


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1) if match else ""
