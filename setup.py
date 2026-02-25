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
from setuptools import setup, find_packages

setup(
    name="niki-doc-ai",
    version="2.0.0",
    description="Niki-docAI: AI-Centric Documentation Automation Tool",
    author="Niki-docAI Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "watchdog>=6.0.0",
        "tree-sitter>=0.23.2",
        "colorama>=0.4.6",
        "pathspec>=0.12.1",
    ],
    entry_points={
        "console_scripts": [
            "ndoc=ndoc.entry:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Programming Language :: Python :: 3",
    ],
)
