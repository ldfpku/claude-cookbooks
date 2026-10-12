# 评估

针对三个领域中标注好的样本（`data/<domain>/samples.jsonl`）运行完整流程，并把每个结论与其预期标签比对。使用 cookbook 目录中的 `engine.py` 和 `pipeline.py`，即指南所导入的同一批模块。

```bash
pip install anthropic python-dotenv
# from capabilities/content_moderation/ (needs ANTHROPIC_API_KEY):
python evaluation/run_eval.py
```

ad_creatives 领域使用 `data/ad_creatives/rules.golden.json` 中手写的规则集；另外两个领域在首次运行时由 Claude 编译，并缓存在 `evaluation/compiled/` 下。结果写入 `evaluation/results.json`。
