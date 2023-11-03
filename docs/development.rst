===============================================================================
Developing on local PC
===============================================================================

:ref:`How to contribute<How to contribute>`

Setup environment
*******************************************************************************

1. Install `pyenv <https://github.com/pyenv/pyenv#installation>`_.

2. Prepare interpreter

.. code-block:: console

    $ pyenv install 3.12
    $ pyenv shell $(pyenv latest 3.12)

3. Install dependencies

.. code-block:: console

    $ pip install -U poetry
    $ poetry config virtualenvs.in-project true && poetry install && source .venv/bin/activate

4. Init project

.. code-block:: console

    $ inv project.init


Style checks
*******************************************************************************

.. note::
    For common actions in the project used `invoke <https://pypi.org/project/invoke/>`_.

We use `pre-commit` for quality control.
To run checks:

.. code-block:: console

    $ inv pre-commit.run-hooks

.. note::

    Package also include flake8 dependencies for proper support of flake8 vscode plugin.


Local Documentation
*******************************************************************************

To generate local documentation, use:

.. code-block:: console

    $ inv docs.build

To clear local documentation, use:

.. code-block:: console

    $ inv docs.clear
