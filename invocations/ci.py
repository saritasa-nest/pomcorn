import invoke
import saritasa_invocations


@invoke.task
def prepare(context: invoke.Context) -> None:
    """Prepare ci environment for check."""
    saritasa_invocations.print_success("Preparing CI")
    saritasa_invocations.uv.sync(context)


@invoke.task
def run_pre_commit(context: invoke.Context) -> None:
    """Run pre-commit hooks."""
    saritasa_invocations.pre_commit.run_hooks(context)
