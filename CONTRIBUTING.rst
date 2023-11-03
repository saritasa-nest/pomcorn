===============================================================================
How to contribute
===============================================================================

`Installing <https://read-the-docs-pomcorn.readthedocs.io/en/latest/installation.html>`_

*******************************************************************************
Submitting your code
*******************************************************************************

We use `trunk based <https://trunkbaseddevelopment.com/>`_ development.

What is the point of this method?

1. We use protected `main` branch,
   so the only way to push your code is via pull request
2. We use issue branches: to implement a new feature or to fix a bug
   create a new branch named `issue-$bugname`
3. Then create a pull request to `main` branch
4. We use `git tags` to make releases, so we can track what has changed
   since the latest release

So, this way we achieve an easy and scalable development process
which frees us from merging hell and long-living branches.

In this method, the latest version of the app is always in the `main` branch.

-------------------------------------------------------------------------------
Before submitting
-------------------------------------------------------------------------------

Before submitting your code please do the following steps:

1. Add any changes you want
2. Edit the documentation if you have changed something significant
3. Update `CHANGELOG.rst <https://github.com/saritasa-nest/pomcorn/blob/main/docs/CHANGELOG.rst>`_ with a quick summary of your changes
4. Run `pre-commit <https://pomcorn.readthedocs.io/en/latest/development.html#style-checks>`_ to ensure that style is correct
