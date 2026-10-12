# Orchestrate：把一个 issue 推进到已合并的 PR

这是一个自包含的维护者工作流模拟，供 `CMA_orchestrate_issue_to_pr.py` 使用。cookbook 会把该目录打包并交给智能体。

- `gh-mock`，一个 bash 脚本，模拟相关的 `gh` 子命令。状态保存在 `.gh-state/` 中。
- `issue_42.json`，一份 Unicode 缺陷报告（`Café Culture` → `caf-culture`）。描述足够含糊，智能体必须阅读代码。
- `src/url_utils.py` + `src/blog.py` + `tests/test_urls.py`，有缺陷的 `slugify()` 以及能捕获问题的失败测试。

其中埋入了两个恢复点：第一次不完整的修复会让 CI 失败并给出 pytest 回溯；如果 `slugify()` 缺少 docstring，模拟的审查机器人会阻止合并。一次顺利的运行结束时，`.gh-state/pr_101.json` 会显示 `state: merged`、`ci/test: pass`，以及一条 `APPROVED` 审查。
