from setuptools import setup, find_packages, find_namespace_packages
from setuptools.command.install import install
import subprocess
import sys
import os
import time

class PostInstallCommand(install):
    def run(self):
        install.run(self)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="debugbuddy-cli",
    version="0.2.2",
    license='MIT',
    author="DevArqf",
    author_email="devarqf@gmail.com",
    description="Your terminal's debugging companion - instant error explanations",
    long_description_content_type="text/markdown",
    url="https://github.com/DevArqf/DeBugBuddy",
    download_url="https://github.com/DevArqf/DeBugBuddy/archive/refs/tags/v0.2.2.tar.gz",
    keywords = ['python', 'debugging', 'cli'],
    packages=find_namespace_packages(include=['debugbuddy', 'debugbuddy.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
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
        "openai>=2.8.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "ai": [
            "anthropic>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dbug=debugbuddy.cli:main",
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