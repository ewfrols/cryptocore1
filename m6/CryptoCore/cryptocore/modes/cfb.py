"""
CFB (Cipher Feedback) Mode
"""

from cryptography.hazmat.primitives.ciphers import modes
from .base_mode import BaseMode  # Изменено с БазовыйРежим на BaseMode


class CFB(BaseMode):  # Изменено с БазовыйРежим на BaseMode
    """CFB (Cipher Feedback) Mode"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает объект режима CFB"""
        if iv is None:
            raise ValueError("Для режима CFB требуется IV")
        return modes.CFB(iv)