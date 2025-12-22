"""
ECB (Electronic Codebook) Mode
"""

from cryptography.hazmat.primitives.ciphers import modes
from .base_mode import BaseMode  # Изменено с БазовыйРежим на BaseMode


class ECB(BaseMode):  # Изменено с БазовыйРежим на BaseMode
    """ECB (Electronic Codebook) Mode"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает объект режима ECB"""
        return modes.ECB()