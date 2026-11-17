# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = 'ORIGAMI'
copyright = "2026, DESI-UR"
author = "DESI-UR"

# The short X.Y version
version = '2.0'
# The full version, including alpha/beta/rc tags
release = '2.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
    'myst_parser',      # lets the .rst pages include the Markdown README
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

myst_enable_extensions = [
    'dollarmath',   # $...$ and $$...$$ math
    'colon_fence',  # ::: note blocks
    'deflist',
]
myst_heading_anchors = 3    # makes links like README.md#section work

# Add any paths that contain templates here, relative to this directory.
templates_path = ['.templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

#html_logo = 'filename.png'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_title = 'ORIGAMI'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['.static']
html_css_files = ['custom.css']
