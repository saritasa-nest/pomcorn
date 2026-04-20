import invoke
import saritasa_invocations

import invocations

ns = invoke.Collection(
    invocations.ci,
    invocations.docs,
    invocations.project,
    saritasa_invocations.pytest,
    saritasa_invocations.poetry,
    saritasa_invocations.git,
    saritasa_invocations.pre_commit,
    saritasa_invocations.mypy,
    saritasa_invocations.python,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            project_name="pomcorn",
        ),
    },
)
