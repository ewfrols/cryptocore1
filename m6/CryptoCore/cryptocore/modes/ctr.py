"""
CTR (Counter) Mode
"""

from cryptography.hazmat.primitives.ciphers import modes
from .base_mode import BaseMode  # Изменено с БазовыйРежим на BaseMode


class CTR(BaseMode):  # Изменено с БазовыйРежим на BaseMode
    """CTR (Counter) Mode"""
    
    def _создать_режим(self, iv: bytes = None):
        """Создает объект режима CTR"""
        if iv is None:
            raise ValueError("Для режима CTR требуется nonce")
        return modes.CTR(iv)