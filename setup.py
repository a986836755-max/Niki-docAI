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
        "colorama>=0.4.6",
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
