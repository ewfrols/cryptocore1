"""
CryptoCore - Cryptographic toolkit
"""

__version__ = "0.4.0"
__author__ = "CryptoCore Team"

# Основные экспорты
from .main import main
from .cli_parser import parse_arguments

# Для обратной совместимости
try:
    ПарсерАргументов = parse_arguments
except:
    pass

__all__ = ['main', 'parse_arguments']