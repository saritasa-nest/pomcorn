===============================================================================
Installation
===============================================================================

Requirements
*******************************************************************************

Pomcorn requires Python >= 3.11 and Selenium >= 4.12.

Install Pomcorn
*******************************************************************************
You can install it by **pip**:

.. code-block:: console

   $ pip install pomcorn

Or **poetry**:

.. code-block:: console

   $ poetry add pomcorn

Additional dependencies
*******************************************************************************

In order for Selenium to interact with the browser, you need to install the webdriver for that browser.

Chrome Driver
-------------------------------------------------------------------------------

For Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Double `__` is used to create an anonymous link and skip sphinx error
  `Duplicate explicit target name` for `Chrome Driver`

* Via Chocolatey:
    1. Install `Chrome Driver <https://chocolatey.org/packages/chromedriver>`__.
    2. Open the `powershell` as `admin`

    .. code-block:: console

        $ choco install chromedriver

* Manually:
    1. Install `Chrome Driver <https://sites.google.com/a/chromium.org/chromedriver/home>`__.
    2. Unzip and put ``.exe`` in ``C:\Windows`` or add the path to your webdriver in the ``PATH`` system variable:

    .. code-block:: console

        $ export PATH=$PATH:/path/to/driver/browser-driver

For Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Via package managers:
    * Install `Chrome Driver <https://command-not-found.com/chromedriver>`__.
    * Install `Chromium (comes with the same driver as Chrome Driver) <https://command-not-found.com/chromium>`__.
* Manually:
    * Install `Chrome Driver <https://sites.google.com/a/chromium.org/chromedriver/home>`__.

For Mac
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Via brew:
    1. Install `Chrome Driver <https://formulae.brew.sh/cask/chromedriver>`__.
    2. Use brew:

    .. code-block:: console

        $ brew install chromedriver

* Manually:
    * Install `Chrome Driver <https://sites.google.com/a/chromium.org/chromedriver/home>`__.
