"""
Режим Cipher Block Chaining (CBC)
"""

from .base_mode import БазовыйРежим
from cryptography.hazmat.primitives.ciphers import modes


class CBC(БазовыйРежим):
    """Режим Cipher Block Chaining"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает режим CBC"""
        if iv is None:
            raise ValueError("Для режима CBC требуется IV")
        return modes.CBC(iv)
