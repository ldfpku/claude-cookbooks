# 嵌入向量
文本嵌入向量是文本字符串的数值化表示，表现为一串浮点数构成的向量。我们可以用两个文本嵌入向量之间的距离（常用的是余弦相似度）来衡量两段文本彼此相关的程度，距离越小意味着相关性越高。

比较字符串之间的相似度，或者按彼此距离对字符串聚类，可以支撑很多类应用，包括**搜索**（在 RAG 架构中很流行）、**推荐**和**异常检测**。

## 如何用 Anthropic 获取嵌入向量
虽然 Anthropic 不提供自己的嵌入模型，但我们已与 [Voyage AI](https://www.voyageai.com/?ref=anthropic) 合作，作为文本嵌入的首选提供方。Voyage 开发了[处于业界前沿](https://blog.voyageai.com/2023-10-29/voyage-embeddings/?ref=anthropic)的嵌入模型，甚至提供针对金融、医疗等特定行业定制的模型，以及可以针对你的公司微调的模型。

要使用 Voyage 嵌入向量，请先在 [Voyage AI 官网](https://dash.voyageai.com/?ref=anthropic) 注册，获取一个 API 密钥，并把该 API 密钥设置为环境变量以便使用：

```bash
export VOYAGE_API_KEY="<your secret key>"
```

你可以使用官方 [﷐0﷑ Python 包](https://github.com/voyage-ai/voyageai-python) 或 HTTP 请求获取嵌入向量，如下文所述。

### Voyage Python 包

`voyageai` 包可以用以下命令安装：

```bash
pip install -U voyageai
```

然后，你可以创建一个客户端对象，并开始用它对文本生成嵌入向量：

```python
import voyageai

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

texts = ["Sample text 1", "Sample text 2"]

result = vo.embed(texts, model="voyage-2", input_type="document")
print(result.embeddings[0])
print(result.embeddings[1])
```

`result.embeddings` 将是包含两个嵌入向量的列表，每个向量含 1024 个浮点数。运行上述代码后，两个嵌入向量会打印在屏幕上：

```
[0.02012746, 0.01957859, ...]  # embedding for "Sample text 1"
[0.01429677, 0.03077182, ...]  # embedding for "Sample text 2"
```

创建嵌入向量时，你可以给 `embed()` 函数指定若干其他参数。以下是其规格说明：

> `voyageai.Client.embed(texts : List[str], model : str = "voyage-2", input_type : Optional[str] = None, truncation : Optional[bool] = None)`

- **texts**（List[str]）——文本列表，即字符串构成的列表，例如 `["I like cats", "I also like dogs"]`。目前列表的最大长度为 128，列表中词元总数在 `voyage-2` 上最多为 320K，在 `voyage-code-2` 上最多为 120K。
- **model**（str）——模型名称。推荐选项：`voyage-2`（默认）、`voyage-code-2`。
- **input_type**（str，可选，默认为 `None`）——输入文本的类型。默认为 `None`。其他选项：`query`、`document`。
    - 当 input_type 设置为 `None` 时，输入文本会被我们的嵌入模型直接编码。而当输入是文档或查询时，用户可以分别把 input_type 指定为 `query` 或 `document`。这种情况下，Voyage 会在输入文本前加上一条特殊提示词，并把扩展后的输入发送给嵌入模型。
    - 对于检索/搜索类用例，我们建议在编码查询或文档时指定该参数，以提升检索质量。带与不带 input_type 参数生成的嵌入向量是相互兼容的。

- **truncation**（bool，可选，默认为 `None`）——是否截断输入文本以适配上下文长度。
    - 如果为 `True`，超长的输入文本会在被嵌入模型向量化之前截断，以适配上下文长度。
    - 如果为 `False`，当任何给定文本超出上下文长度时会抛出错误。
    - 如果未指定（默认为 `None`），当输入文本略微超出上下文窗口长度时，Voyage 会在发送给嵌入模型之前先截断它；如果显著超出上下文窗口长度，则抛出错误。

### Voyage HTTP API

你也可以通过请求 Voyage HTTP API 获取嵌入向量。例如，可以在终端中用 `curl` 命令发送一次 HTTP 请求：

```bash
curl https://api.voyageai.com/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VOYAGE_API_KEY" \
  -d '{
    "input": ["Sample text 1", "Sample text 2"],
    "model": "voyage-2"
  }'
```

你会得到的响应是一个 JSON 对象，其中包含嵌入向量和词元用量：

```bash
{
  "object": "list",
  "data": [
    {
      "embedding": [0.02012746, 0.01957859, ...],
      "index": 0
    },
    {
      "embedding": [0.01429677, 0.03077182, ...],
      "index": 1
    }
  ],
  "model": "voyage-2",
  "usage": {
    "total_tokens": 10
  }
}
```

Voyage AI 的嵌入端点是 `https://api.voyageai.com/v1/embeddings`（POST）。请求头必须包含 API 密钥。请求体是一个 JSON 对象，包含以下参数：

- **input**（str，List[str]）——单个文本字符串，或由字符串构成的文本列表。目前列表的最大长度为 128，列表中词元总数在 `voyage-2` 上最多为 320K，在 `voyage-code-2` 上最多为 120K。
- **model**（str）——模型名称。推荐选项：`voyage-2`（默认）、`voyage-code-2`。
- **input_type**（str，可选，默认为 `None`）——输入文本的类型。默认为 `None`。其他选项：`query`、`document`。
- **truncation**（bool，可选，默认为 `None`）——是否截断输入文本以适配上下文长度。
    - 如果为 `True`，超长的输入文本会在被嵌入模型向量化之前截断，以适配上下文长度。
    - 如果为 `False`，当任何给定文本超出上下文长度时会抛出错误。
    - 如果未指定（默认为 `None`），当输入文本略微超出上下文窗口长度时，Voyage 会在发送给嵌入模型之前先截断它；如果显著超出上下文窗口长度，则抛出错误。
- **encoding_format**（str，可选，默认为 `None`）——嵌入向量的编码格式。Voyage 目前支持两种选项：
    - 如果未指定（默认为 `None`）：嵌入向量以浮点数列表表示；
    - `"base64"`：嵌入向量被压缩为 [Base64](https://docs.python.org/3/library/base64.html) 编码。


### AWS Marketplace

Voyage 嵌入向量可在 [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=seller-snt4gb6fd7ljg) 获取。以下是在 AWS 上访问 Voyage 的说明：

1. 订阅模型包

    1. 前往[模型包列表页面](https://aws.amazon.com/marketplace/seller-profile?id=seller-snt4gb6fd7ljg)并选择要部署的模型。
    1. 点击 *Continue to subscribe* 按钮。
    1. 在 *Subscribe to this software* 页面上，请仔细审阅各项细节。如果你和你的组织认可标准最终用户许可协议（EULA）、定价与支持条款，请点击 "Accept Offer"。
    1. 选择 *Continue to configuration* 并选定一个区域后，你会看到一个 Product Arn。这就是用 Boto3 创建可部署模型所需的模型包 ARN。复制与你所选区域对应的 ARN，并在后续单元格中使用它。

2. 部署模型包

    从这一步开始，我们建议你继续使用我们提供的[笔记本](https://github.com/voyage-ai/voyageai-aws/blob/main/notebooks/deploy_voyage_code_2_sagemaker.ipynb)，它位于 [Sagemaker Studio](https://aws.amazon.com/sagemaker/studio/)。请创建一个 JupyterLab 空间，上传我们的笔记本，然后从那里继续。


## 可用模型

Voyage 推荐使用以下嵌入模型：

| 模型 | 上下文长度 | 嵌入向量维度 | 说明 |
| --- | --- | --- | --- |
| `voyage-2` | 4000 | 1024 | 最新的基线（通才）嵌入模型，检索质量最佳。详见[博客文章](https://blog.voyageai.com/2023-10-29/voyage-embeddings/?ref=anthropic)。|
| `voyage-code-2` | 16000 | 1536 | 针对代码检索优化（比替代方案好 17%），在通用语料上同样处于业界前沿。详见[博客文章](https://blog.voyageai.com/2024-01-23/voyage-code-2-elevate-your-code-retrieval/?ref=anthropic)。|

`voyage-2` 是一个通才嵌入模型，在各领域都达到业界前沿水平，同时保持高效率。`voyage-code-2` 针对代码应用优化，提供 4 倍的上下文长度以便更灵活地使用，代价是时延略高。

Voyage 正在积极开发更先进、更专门的模型，并可以为你的公司微调嵌入向量。如需试用权限或在你自己的数据上微调，请发邮件至 [contact@voyageai.com](mailto:contact@voyageai.com)！

- `voyage-finance-2`：即将推出
- `voyage-law-2`：即将推出
- `voyage-multilingual-2`：即将推出
- `voyage-healthcare-2`：即将推出

## 动机示例
既然已经知道如何获取嵌入向量，我们来看一个简单的动机示例。

假设我们有一个由六篇文档组成的小型语料库，需要从中进行检索：

```python
documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature."
]
```

我们首先使用 Voyage 把每篇文档转换为一个嵌入向量

```python
import voyageai

vo = voyageai.Client()

# Embed the documents
doc_embds = vo.embed(
    documents, model="voyage-2", input_type="document"
).embeddings
```

这些嵌入向量让我们能够在向量空间中执行语义搜索/检索。给定一个示例查询，

```python
query = "When is Apple's conference call scheduled?"
```

我们把它转换为嵌入向量，并进行最近邻搜索，以找出在嵌入空间距离意义上最相关的文档。

```python
import numpy as np

# Embed the query
query_embd = vo.embed(
    [query], model="voyage-2", input_type="query"
).embeddings[0]

# Compute the similarity
# Voyage embeddings are normalized to length 1, therefore dot-product
# and cosine similarity are the same.
similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
```

请注意，我们对文档和查询分别使用 `input_type="document"` 和 `input_type="query"`。更多说明请见[这里](#voyage-python-package)。

输出结果会是第 5 篇文档，它确实与该查询最相关：

```
Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.
```

如果你在寻找关于如何用嵌入向量做 RAG 的详细 cookbook 集合，包括向量数据库，请参阅我们的 [RAG cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Pinecone/rag_using_pinecone.ipynb)。

## 常见问题
### 如何计算两个嵌入向量之间的距离？
余弦相似度是常见的选择，但大多数距离函数都足够好用。Voyage 的嵌入向量已归一化为长度 1，因此余弦相似度本质上等同于两个向量之间的点积。下面是一段可用于计算两个嵌入向量之间余弦相似度的代码片段。

```python
import numpy

similarity = np.dot(embd1, embd2)
# Voyage embeddings are normalized to length 1, therefore cosine similarity
# is the same as dot-product.
```

如果你想在大型语料库上查找 K 个最近邻嵌入向量，我们建议使用大多数向量数据库内置的能力。

### 我能在嵌入之前统计字符串中的词元数量吗？
可以！你可以用下面的代码做到这一点。

```python
import voyageai

vo = voyageai.Client()
total_tokens = vo.count_tokens(["Sample text"])
```

## 定价
定价信息可在 Voyage 网站的[定价页面](https://docs.voyageai.com/pricing/?ref=anthropic)上获取，应以该页面为准。
