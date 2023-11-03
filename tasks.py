import saritasa_invocations
from invoke.collection import Collection

import invocations as local_invocations

ns = Collection(
    local_invocations.docs,
    local_invocations.project,
    saritasa_invocations.git,
    saritasa_invocations.mypy,
    saritasa_invocations.pytest,
    saritasa_invocations.pre_commit,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
    },
)
