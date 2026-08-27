import os

import invoke
import saritasa_invocations

import invocations

ns = invoke.Collection(
    invocations.ci,
    invocations.docs,
    invocations.project,
    saritasa_invocations.pytest,
    saritasa_invocations.uv,
    saritasa_invocations.git,
    saritasa_invocations.pre_commit,
    saritasa_invocations.mypy,
    saritasa_invocations.python,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": os.environ.get("INVOKE_PTY", "true").lower() == "true",
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            project_name="pomcorn",
            pre_commit=saritasa_invocations.PreCommitSettings(
                entry="prek",
                default_hook_stage="pre-push",
            ),
        ),
    },
)
