"""
Módulo de utilidades.
Funciones auxiliares para la aplicación.
"""

from datetime import datetime
from typing import Optional


def format_datetime(iso_string: str) -> str:
    """
    Formatea una fecha ISO a un formato legible.
    
    Args:
        iso_string: Fecha en formato ISO string
        
    Returns:
        Fecha formateada como string legible
    """
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return iso_string


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Trunca un texto si excede la longitud máxima.
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima permitida
        
    Returns:
        Texto truncado con "..." si fue necesario
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."

