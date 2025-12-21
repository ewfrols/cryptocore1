"""
Режим Cipher Feedback (CFB)
"""

from .base_mode import БазовыйРежим
from cryptography.hazmat.primitives.ciphers import modes


class CFB(БазовыйРежим):
    """Режим Cipher Feedback"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает режим CFB"""
        if iv is None:
            raise ValueError("Для режима CFB требуется IV")
        return modes.CFB(iv)
