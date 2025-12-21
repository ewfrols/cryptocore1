"""
Режим Counter (CTR)
"""

from .base_mode import БазовыйРежим
from cryptography.hazmat.primitives.ciphers import modes


class CTR(БазовыйРежим):
    """Режим Counter"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает режим CTR"""
        if iv is None:
            raise ValueError("Для режима CTR требуется IV")
        return modes.CTR(iv)
