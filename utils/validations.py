import re

def validate_email(email):
    """Valida el formato de un correo electrónico"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_survey_response(pregunta_tipo, respuesta):
    """Valida que una respuesta sea adecuada según el tipo de pregunta"""
    if pregunta_tipo == 'calificacion_1_5':
        return isinstance(respuesta, int) and 1 <= respuesta <= 5
    elif pregunta_tipo in ['texto_corto', 'texto_largo']:
        return isinstance(respuesta, str) and len(respuesta.strip()) > 0
    return False

def sanitize_filename(filename):
    """Limpia un nombre de archivo de caracteres no válidos"""
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)