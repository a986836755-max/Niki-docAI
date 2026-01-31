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
        "tree-sitter-python>=0.23.6",
        "tree-sitter-cpp>=0.23.4",
        "tree-sitter-javascript>=0.23.1",
        "tree-sitter-typescript>=0.23.2",
        "tree-sitter-go>=0.23.4",
        "tree-sitter-rust>=0.23.2",
        "tree-sitter-dart>=0.23.2",
        "tree-sitter-c-sharp>=0.23.1",
        "tree-sitter-java>=0.23.5",
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
