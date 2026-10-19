# Iterate：让测试全部转绿

一个 `calc.py`，其中埋入三个缺陷；一个 `test_calc.py`，其中有三条能捕获这些缺陷的断言。供 `CMA_iterate_fix_failing_tests.py` 使用。

有意思的缺陷是 `test_mean`：`mean()` 内部调用 `add` 和 `divide`，因此另外两个修好后它自己就会转绿。直接修改 `mean()` 的智能体属于过度修复。
