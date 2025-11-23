from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os
import time

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.call([sys.executable, '-c', '''
import os
import sys
import time

os.system('cls' if os.name == 'nt' else 'clear')

print("\\033[92m")
print("██████╗ ███████╗██████╗ ██╗   ██╗ ██████╗ ██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗")
print("██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝ ██╔══██╗██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝")
print("██║  ██║█████╗  ██████╔╝██║   ██║██║  ███╗██████╔╝██║   ██║██║  ██║██║  ██║ ╚████╔╝ ")
print("██║  ██║██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██╗██║   ██║██║  ██║██║  ██║  ╚██╔╝  ")
print("██████╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ")
print("╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ")
print("\\033[0m")

print("\\033[96m                    Your Terminal's Debugging Companion\\033[0m")
print("\\033[2m                          Made with ❤️  by DevArqf\\033[0m\\n")

spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
for i in range(15):
    for char in spinner:
        sys.stdout.write(f'\\r\\033[92m{char}\\033[0m Setting up DeBugBuddy...')
        sys.stdout.flush()
        time.sleep(0.05)

sys.stdout.write('\\r\\033[92m✓\\033[0m Setting up DeBugBuddy...\\n')
sys.stdout.flush()

print("\\n\\033[92m✅ DeBugBuddy installed successfully!\\033[0m\\n")

print("\\033[96m🎯 Quick Start:\\033[0m\\n")
print("  \\033[93m1. Explain an error:\\033[0m")
print("     \\033[2mdb explain \\"NameError: name 'x' is not defined\\"\\033[0m\\n")

print("  \\033[93m2. Interactive mode:\\033[0m")
print("     \\033[2mdb interactive\\033[0m\\n")

print("  \\033[93m3. Watch directory:\\033[0m")
print("     \\033[2mdb watch src/\\033[0m\\n")

print("  \\033[93m4. View history:\\033[0m")
print("     \\033[2mdb history\\033[0m\\n")

print("\\033[96m💡 Tips:\\033[0m")
print("  • Run \\033[92mdb --help\\033[0m to see all commands")
print("  • Use \\033[92mdb explain -e\\033[0m to see code examples")
print("  • Type \\033[92mdb config --show\\033[0m to view settings\\n")

print("\\033[92m🐛💬 Ready to debug smarter? Try it now!\\033[0m\\n")
print("\\033[2m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\033[0m")
print("\\033[2mGitHub: https://github.com/DevArqf/DeBugBuddy\\033[0m")
print("\\033[2mDocs:   https://github.com/DevArqf/DeBugBuddy#readme\\033[0m")
print("\\033[2m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\033[0m\\n")
'''])

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="debugbuddy",
    version="0.1.1",
    license='MIT',
    author="DevArqf",
    author_email="devarqf@gmail.com",
    description="Your terminal's debugging companion - instant error explanations",
    long_description_content_type="text/markdown",
    url="https://github.com/DevArqf/DeBugBuddy",
    download_url="https://github.com/DevArqf/DeBugBuddy/archive/refs/tags/v0.1.1.tar.gz",
    keywords = ['python', 'debugging', 'cli'],
    packages=find_packages(),
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