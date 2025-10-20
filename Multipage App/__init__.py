# app/__init__.py
"""
Jornada de Ingeniería Industrial - Sistema de Constancias
"""

__version__ = "1.0.0"

# app/utils/__init__.py
"""
Módulo de utilidades
"""

from .data_handler import DataHandler
from .pdf_generator import PDFGenerator
from .validations import validate_email, validate_survey_response

__all__ = [
    'DataHandler',
    'PDFGenerator',
    'validate_email',
    'validate_survey_response'
]

# app/pages/__init__.py
"""
Módulo de páginas
"""