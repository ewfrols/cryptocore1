"""
Базовый класс для всех режимов шифрования
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import abc


class БазовыйРежим(abc.ABC):
    """Абстрактный базовый класс для режимов шифрования AES"""
    
    def __init__(self, ключ):
        """
        Инициализирует режим шифрования
        
        Args:
            ключ: Ключ шифрования (16 байт) в формате bytes или hex-строка
        """
        # Преобразуем ключ в bytes если нужно
        if isinstance(ключ, bytes):
            self.ключ = ключ
        elif isinstance(ключ, str):
            # Это hex-строка
            self.ключ = bytes.fromhex(ключ)
        else:
            raise ValueError(f"Неверный тип ключа: {type(ключ)}. Ожидается bytes или str")
        
        # Проверяем длину ключа
        if len(self.ключ) != 16:
            raise ValueError(f"Ключ должен быть 16 байт, получено {len(self.ключ)} байт")
    
    @abc.abstractmethod
    def _создать_режим(self, iv: bytes = None):
        """Создает объект режима шифрования (должен быть реализован в подклассе)"""
        pass
    
    def зашифровать(self, данные: bytes, iv: bytes = None) -> bytes:
        """Шифрует данные"""
        режим = self._создать_режим(iv)
        cipher = Cipher(algorithms.AES(self.ключ), режим, backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Для режима CBC добавляем padding
        if isinstance(режим, modes.CBC):
            padder = padding.PKCS7(128).padder()
            данные = padder.update(данные) + padder.finalize()
        
        return encryptor.update(данные) + encryptor.finalize()
    
    def расшифровать(self, данные: bytes, iv: bytes = None) -> bytes:
        """Расшифровывает данные"""
        режим = self._создать_режим(iv)
        cipher = Cipher(algorithms.AES(self.ключ), режим, backend=default_backend())
        decryptor = cipher.decryptor()
        
        данные = decryptor.update(данные) + decryptor.finalize()
        
        # Для режима CBC убираем padding
        if isinstance(режим, modes.CBC):
            unpadder = padding.PKCS7(128).unpadder()
            данные = unpadder.update(данные) + unpadder.finalize()
        
        return данные