"""
Режим Output Feedback (OFB)
"""

from .base_mode import БазовыйРежим
from cryptography.hazmat.primitives.ciphers import modes


class OFB(БазовыйРежим):
    """Режим Output Feedback"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает режим OFB"""
        if iv is None:
            raise ValueError("Для режима OFB требуется IV")
        return modes.OFB(iv)
