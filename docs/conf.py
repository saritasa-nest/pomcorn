# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup ---------------------------------------------------------------
import pathlib
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use Path.resolve() to make it absolute, like shown here.
sys.path.append(str(pathlib.Path().resolve()))
sys.path.append(str(pathlib.Path("..").resolve()))
sys.path.append(str(pathlib.Path("../").resolve()))

# -- Project information ------------------------------------------------------
from datetime import datetime

project = "Pomcorn"
copyright = f"{datetime.now().year}, Saritasa"  # noqa:A001
author = "Saritasa"

# -- General configuration ---------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom ones.
extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    # Documentation generator
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    # Support for Google style Python docstrings
    "sphinx.ext.napoleon",
    # Support mermaid diagrams
    # https://github.com/mgaitan/sphinxcontrib-mermaid/tree/master
    "sphinxcontrib.mermaid",
]

# Add ability to zoom mermaid diagrams
mermaid_d3_zoom = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# -- Options for HTML output --------------------------------------------------
html_theme = "sphinx_rtd_theme"

html_sidebars = {"**": ["globaltoc.html", "searchbox.html", "relations.html"]}

# -- Autodoc configuration ----------------------------------------------------
autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__,__annotations__",
    "undoc-members": True,
}
