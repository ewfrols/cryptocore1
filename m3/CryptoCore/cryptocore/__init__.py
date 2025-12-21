"""
Пакет CryptoCore для шифрования файлов AES
"""

# Импортируем основные классы для удобства
from .main import main
from .cli_parser import ПарсерАргументов
from .file_io import РаботаСФайлами

# Если есть другие важные импорты, добавьте их здесь

__version__ = "3.0.0"
__author__ = "CryptoCore Team"
__description__ = "Программа для шифрования файлов AES с поддержкой CSPRNG"