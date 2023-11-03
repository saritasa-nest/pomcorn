from pathlib import Path

import invoke
from saritasa_invocations import print_success

LOCAL_DOCS_DIR = Path("local-docs")


@invoke.task
def build(context: invoke.Context):
    """Build documentation to local directory.

    By default, documentation is generated to folder ``LOCAL_DOCS_DIR`` as it
    is specified in ``.gitignore``.

    """
    print_success("Start building of local documentation")
    context.run(f"sphinx-build -E -a docs {LOCAL_DOCS_DIR}")
    print_success("Building completed")


@invoke.task
def clear(context: invoke.Context):
    """Clear folder with local documentation."""
    print_success("Start cleaning of local documentation")
    context.run(f"rm -rf {LOCAL_DOCS_DIR}/*")
    print_success("Cleaning completed")
