"""
Базовый класс для всех режимов шифрования
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import abc


class BaseMode(abc.ABC):  # Изменено с БазовыйРежим на BaseMode
    """Абстрактный базовый класс для режимов шифрования AES"""
    
    def __init__(self, key):
        """
        Инициализирует режим шифрования
        
        Args:
            key: Ключ шифрования (16 байт) в формате bytes или hex-строка
        """
        # Преобразуем ключ в bytes если нужно
        if isinstance(key, bytes):
            self.key = key
        elif isinstance(key, str):
            # Это hex-строка
            self.key = bytes.fromhex(key)
        else:
            raise ValueError(f"Неверный тип ключа: {type(key)}. Ожидается bytes или str")
        
        # Проверяем длину ключа
        if len(self.key) != 16:
            raise ValueError(f"Ключ должен быть 16 байт, получено {len(self.key)} байт")
    
    @abc.abstractmethod
    def _создать_режим(self, iv: bytes = None):
        """Создает объект режима шифрования (должен быть реализован в подклассе)"""
        pass
    
    def encrypt(self, data: bytes, iv: bytes = None) -> bytes:
        """Шифрует данные"""
        режим = self._создать_режим(iv)
        cipher = Cipher(algorithms.AES(self.key), режим, backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Для режима CBC добавляем padding
        if isinstance(режим, modes.CBC):
            padder = padding.PKCS7(128).padder()
            data = padder.update(data) + padder.finalize()
        
        return encryptor.update(data) + encryptor.finalize()
    
    def decrypt(self, data: bytes, iv: bytes = None) -> bytes:
        """Расшифровывает данные"""
        режим = self._создать_режим(iv)
        cipher = Cipher(algorithms.AES(self.key), режим, backend=default_backend())
        decryptor = cipher.decryptor()
        
        data = decryptor.update(data) + decryptor.finalize()
        
        # Для режима CBC убираем padding
        if isinstance(режим, modes.CBC):
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(data) + unpadder.finalize()
        
        return data