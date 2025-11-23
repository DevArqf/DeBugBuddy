from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class PostInstallCommand(install):
    def run(self):
        install.run(self)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="debugbuddy",
    version="0.1.0",
    author="DevArqf",
    author_email="devarqf@gmail.com",
    description="Your terminal's debugging companion - instant error explanations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DevArqf/DeBugBuddy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
        "watchdog>=3.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "ai": [
            "openai>=1.0.0",
            "anthropic>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "db=debugbuddy.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "debugbuddy": ["patterns/*.json", "data/*.json"],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)