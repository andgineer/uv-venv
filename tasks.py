import sys
import os

from invoke import task, Context, Collection

ALLOWED_VERSION_TYPES = ["release", "bug", "feature"]
VENV_DIR = ".venv"
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")


def ver_task_factory(version_type: str):
    @task
    def ver(c: Context):
        """Bump the version."""
        c.run(f"./scripts/verup.sh {version_type}")

    return ver

@task
def uv(c: Context):
    """Install or upgrade uv."""
    c.run("curl -LsSf https://astral.sh/uv/install.sh | sh")

@task
def setup(c: Context):
    """Setup development environment with uv."""
    # Create venv if it doesn't exist
    result = c.run(f"test -d {VENV_DIR}", warn=True, hide=True)
    if result.return_code != 0:
        print("Creating virtual environment...")
        c.run(f"uv venv {VENV_DIR}")

    # Install dependencies
    print("Installing dependencies...")
    c.run("uv pip install -r requirements.dev.txt")

@task
def test(c: Context):
    """Run all tests with pytest."""
    setup(c)
    c.run(f"{VENV_PYTHON} -m pytest")

@task
def test_unit(c: Context):
    """Run unit tests only."""
    setup(c)
    c.run(f"{VENV_PYTHON} -m pytest -m unit")

@task
def test_integration(c: Context):
    """Run integration tests only."""
    setup(c)
    c.run(f"{VENV_PYTHON} -m pytest -m integration")

@task
def test_coverage(c: Context):
    """Run tests with coverage report."""
    setup(c)
    c.run(f"{VENV_PYTHON} -m pytest --cov --cov-report=html --cov-report=term")

@task
def test_fast(c: Context):
    """Run tests excluding slow tests."""
    setup(c)
    c.run(f"{VENV_PYTHON} -m pytest -m 'not slow'")


namespace = Collection.from_module(sys.modules[__name__])
for name in ALLOWED_VERSION_TYPES:
    namespace.add_task(ver_task_factory(name), name=f"ver-{name}")
