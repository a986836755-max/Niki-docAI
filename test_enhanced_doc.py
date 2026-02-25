# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - LSP 适配：所有 IDE 插件相关的语义能力通过 `ndoc.lsp_server` 暴露。
# - 架构感知：IDE 插件应优先使用 `_MAP.md` 和 `_AI.md` 进行语义增强，而非仅依赖语法树。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - LSP 适配：所有 IDE 插件相关的语义能力通过 `ndoc.lsp_server` 暴露。
# - 架构感知：IDE 插件应优先使用 `_MAP.md` 和 `_AI.md` 进行语义增强，而非仅依赖语法树。
# ------------------------------------------------------------------------------
"""
@MODULE TestModule
This is a test module for enhanced docstring capture.
It should support multi-line docstrings and tags.
@VERSION 1.0.0
"""

# @CORE
# This is a core function.
# It has multi-line comments.
# @TAG1 arg1
# @TAG2 arg2
def test_func(a: int, b: str) -> bool:
    """
    Inner docstring for test_func.
    @INTERNAL
    """
    return True

class TestClass:
    """
    Test class docstring.
    """
    
    # Multi-line comment for field
    # with a tag.
    # @FIELD_TAG
    field: int = 10
    
    def test_method(self):
        # Comment for method
        # @METHOD_TAG
        pass
