"""
Режим Electronic Codebook (ECB)
"""

from .base_mode import БазовыйРежим
from cryptography.hazmat.primitives.ciphers import modes


class ECB(БазовыйРежим):
    """Режим Electronic Codebook"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает режим ECB (не использует IV)"""
        return modes.ECB()
