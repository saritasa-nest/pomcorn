import invoke
import saritasa_invocations


@invoke.task
def init(context: invoke.Context):
    """Build project from scratch."""
    saritasa_invocations.git.setup(context)
    saritasa_invocations.pre_commit.run_hooks(context)

    saritasa_invocations.print_success("Setup done")
