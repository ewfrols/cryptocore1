"""
OFB (Output Feedback) Mode
"""

from cryptography.hazmat.primitives.ciphers import modes
from .base_mode import BaseMode  # Изменено с БазовыйРежим на BaseMode


class OFB(BaseMode):  # Изменено с БазовыйРежим на BaseMode
    """OFB (Output Feedback) Mode"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает объект режима OFB"""
        if iv is None:
            raise ValueError("Для режима OFB требуется IV")
        return modes.OFB(iv)