project = 'Sphinx example'
copyright = '2022, sphinx'
author = 'sphinx'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "furo.sphinxext",
    "sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'furo'
html_static_path = []
