import invoke
from saritasa_invocations import print_success


@invoke.task
def build(context: invoke.Context):
    """Build documentation."""
    print_success("Start building of local documentation")
    context.run("mkdocs build")
    print_success("Building completed")


@invoke.task
def serve(context: invoke.Context):
    """Serve documentation locally."""
    print_success("Start serving local documentation")
    context.run("mkdocs serve")
    print_success("Serving completed")
