import os
import struct
import binascii

class EncryptThenMAC:
    """
    Encrypt-then-MAC AEAD construction.
    Combines any block cipher mode with HMAC for authentication.
    """
    
    def __init__(self, cipher_mode, hmac_key=None, encryption_key=None):
        """
        Initialize Encrypt-then-MAC.
        
        Args:
            cipher_mode: Instance of a block cipher mode (e.g., CTR)
            hmac_key: Key for HMAC (if None, derived from encryption key)
            encryption_key: Key for encryption (if different from HMAC key)
        """
        self.cipher_mode = cipher_mode
        
        # Если не указаны отдельные ключи, используем один ключ для всего
        if encryption_key is None:
            encryption_key = cipher_mode.key
        
        if hmac_key is None:
            # Простое разделение ключа для демонстрации
            # В реальном приложении используйте KDF!
            hmac_key = encryption_key[::-1]  # Обратный ключ
        
        self.encryption_key = encryption_key
        self.hmac_key = hmac_key
        
        # Импортируем HMAC из спринта 5
        from ..mac import HMAC
        self.hmac = HMAC(hmac_key, 'sha256')
    
    def encrypt(self, plaintext, aad=b""):
        """
        Encrypt-then-MAC: C = E(K_e, P), T = MAC(K_m, C || AAD)
        
        Args:
            plaintext: bytes to encrypt
            aad: bytes of associated data
        
        Returns:
            bytes: ciphertext || tag
        """
        # Шаг 1: Шифрование
        ciphertext = self.cipher_mode.encrypt(plaintext)
        
        # Шаг 2: Вычисление MAC над (ciphertext || AAD)
        mac_data = ciphertext + aad
        tag = self.hmac.compute(mac_data)
        
        return ciphertext + tag
    
    def decrypt(self, data, aad=b""):
        """
        Decrypt with MAC verification.
        
        Args:
            data: bytes containing ciphertext || tag
            aad: bytes of associated data
        
        Returns:
            bytes: plaintext if authentication succeeds
        
        Raises:
            AuthenticationError: if MAC verification fails
        """
        # Разделяем ciphertext и tag
        # HMAC-SHA256 produces 32-byte tag
        tag_length = 32
        if len(data) < tag_length:
            raise ValueError("Data too short to contain tag")
        
        ciphertext = data[:-tag_length]
        received_tag = data[-tag_length:]
        
        # Проверяем MAC
        mac_data = ciphertext + aad
        computed_tag = self.hmac.compute(mac_data)
        
        if computed_tag != received_tag:
            raise AuthenticationError("MAC verification failed")
        
        # Если MAC верен, расшифровываем
        return self.cipher_mode.decrypt(ciphertext)


class AuthenticationError(Exception):
    """Exception raised when authentication fails."""
    pass