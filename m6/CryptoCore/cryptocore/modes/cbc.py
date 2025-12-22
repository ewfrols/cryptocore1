"""
CBC (Cipher Block Chaining) Mode
"""

from cryptography.hazmat.primitives.ciphers import modes
from .base_mode import BaseMode  # Изменено с БазовыйРежим на BaseMode


class CBC(BaseMode):  # Изменено с БазовыйРежим на BaseMode
    """CBC (Cipher Block Chaining) Mode"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает объект режима CBC"""
        if iv is None:
            raise ValueError("Для режима CBC требуется IV")
        return modes.CBC(iv)