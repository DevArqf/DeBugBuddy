import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(command, cwd, env=None):
    print(f"Running: {' '.join(str(c) for c in command)}")
    result = subprocess.run(command, cwd=cwd, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}")


def clean_dist(root: Path):
    for name in ["dist", "build"]:
        shutil.rmtree(root / name, ignore_errors=True)
    for path in root.glob("*.egg-info"):
        shutil.rmtree(path, ignore_errors=True)


def build_package(root: Path):
    dist_dir = root / "dist"
    dist_dir.mkdir(exist_ok=True)
    local_build = root / "build.py"
    used_setup = False
    if not local_build.exists():
        try:
            __import__("build")
            run([sys.executable, "-m", "build"], cwd=root)
        except Exception:
            used_setup = True
    else:
        used_setup = True

    if used_setup:
        run([sys.executable, "setup.py", "sdist", "bdist_wheel"], cwd=root)


def create_venv(venv_dir: Path):
    if venv_dir.exists():
        shutil.rmtree(venv_dir, ignore_errors=True)
    run([sys.executable, "-m", "venv", str(venv_dir)], cwd=venv_dir.parent)


def venv_python(venv_dir: Path) -> Path:
    if sys.platform.startswith("win"):
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def install_wheel(venv_dir: Path, wheel_path: Path):
    python_path = venv_python(venv_dir)
    run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"], cwd=venv_dir)
    run([str(python_path), "-m", "pip", "install", "--force-reinstall", str(wheel_path)], cwd=venv_dir)


def run_tests(root: Path):
    run([sys.executable, "-m", "pytest", "-q", "tests/unit", "tests/integration"], cwd=root)


def run_smoke(root: Path, python_path: Path):
    run([str(python_path), "-m", "debugbuddy", "--version"], cwd=root)
    run(
        [
            str(python_path),
            "-m",
            "debugbuddy",
            "explain",
            "NoMethodError: undefined method 'name' for nil:NilClass",
            "--language",
            "ruby",
        ],
        cwd=root,
    )


def list_artifacts(root: Path):
    dist = root / "dist"
    if not dist.exists():
        return []
    return sorted(p.name for p in dist.glob("*"))


def main():
    parser = argparse.ArgumentParser(description="Build DeBugBuddy package artifacts.")
    parser.add_argument("--clean", action="store_true", help="Clean dist/build artifacts first")
    parser.add_argument("--tests", action="store_true", help="Run unit and integration tests")
    parser.add_argument("--install", action="store_true", help="Install wheel into a temp venv")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests after build")
    parser.add_argument("--full", action="store_true", help="Build, test, install, and smoke test")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    venv_dir = root / ".venv_build"

    if args.clean or args.full:
        clean_dist(root)

    build_package(root)

    artifacts = list_artifacts(root)
    if not artifacts:
        raise RuntimeError("No build artifacts found in dist/.")

    print("Build artifacts:")
    for name in artifacts:
        print(f"  - {name}")

    wheel = next((root / "dist" / name for name in artifacts if name.endswith(".whl")), None)
    if not wheel:
        print("No wheel found; skipping install/smoke steps.")
        return

    if args.full:
        args.tests = True
        args.install = True
        args.smoke = True

    if args.tests:
        run_tests(root)

    python_path = sys.executable
    if args.install or args.smoke:
        create_venv(venv_dir)
        install_wheel(venv_dir, wheel)
        python_path = venv_python(venv_dir)

    if args.smoke:
        run_smoke(root, python_path)


if __name__ == "__main__":
    main()
