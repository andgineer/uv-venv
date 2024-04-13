import sys

from invoke import task, Context, Collection

ALLOWED_VERSION_TYPES = ["release", "bug", "feature"]


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


namespace = Collection.from_module(sys.modules[__name__])
for name in ALLOWED_VERSION_TYPES:
    namespace.add_task(ver_task_factory(name), name=f"ver-{name}")
