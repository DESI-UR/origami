# Configuration file for the Sphinx documentation builder.

project = "ORIGAMI"
author = "DESI-UR"          # not sure who to put 
copyright = "2026, DESI-UR" 
release = "2.0"

extensions = [
    "myst_parser",          # lets you write pages in Markdown
    "sphinx.ext.mathjax",   # LaTeX math support if needed 
]

# Accept both Markdown and reStructuredText
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "dollarmath",   # $...$ and $$...$$ math
    "colon_fence",  # ::: note blocks
    "deflist",
]
myst_heading_anchors = 3    # makes links like README.md#section work

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_title = "ORIGAMI"
