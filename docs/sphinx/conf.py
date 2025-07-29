"""
Sphinx configuration file for AUDITORIA360 API documentation.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../src'))

# Project information
project = 'AUDITORIA360'
copyright = '2024, AUDITORIA360 Team'
author = 'AUDITORIA360 Team'
release = '1.0.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
]

# Templates path
templates_path = ['_templates']

# List of patterns to exclude
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Language
language = 'pt_BR'

# HTML output options
html_theme = 'alabaster'
html_static_path = ['_static']

# autodoc options
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Mock imports for modules that might not be available during doc build
autodoc_mock_imports = [
    'fastapi',
    'uvicorn',
    'sqlalchemy',
    'psycopg2',
    'duckdb',
    'pandas',
    'boto3',
    'paddleocr',
    'paddlepaddle',
    'prefect',
    'streamlit',
    'plotly',
    'redis',
    'jose',
    'passlib',
    'pydantic',
    'pytest',
    'playwright',
    'scikit-learn',
]