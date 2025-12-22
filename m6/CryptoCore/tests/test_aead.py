import unittest
import os
import tempfile
import binascii

from cryptocore.crypto.aead.encrypt_then_mac import EncryptThenMAC, AuthenticationError
from cryptocore.modes.ctr import CTR
from cryptocore.crypto.aes_core import AES

class TestEncryptThenMAC(unittest.TestCase):
    """Тесты для Encrypt-then-MAC AEAD (Sprint 6)."""
    
    def test_encrypt_then_mac_basic(self):
        """Basic Encrypt-then-MAC."""
        key = os.urandom(16)
        plaintext = b"Secret message"
        aad = b"associated data"
        
        # Create CTR mode for encryption
        aes = AES(key)
        ctr = CTR(aes, os.urandom(16))
        
        # Create Encrypt-then-MAC
        etm = EncryptThenMAC(ctr)
        
        # Encrypt
        ciphertext = etm.encrypt(plaintext, aad)
        
        # Decrypt
        decrypted = etm.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ Basic Encrypt-then-MAC passed")
    
    def test_encrypt_then_mac_aad_tamper(self):
        """Encrypt-then-MAC should detect wrong AAD."""
        key = os.urandom(16)
        plaintext = b"Message"
        correct_aad = b"correct"
        wrong_aad = b"wrong"
        
        aes = AES(key)
        ctr = CTR(aes, os.urandom(16))
        etm = EncryptThenMAC(ctr)
        
        # Encrypt
        ciphertext = etm.encrypt(plaintext, correct_aad)
        
        # Try to decrypt with wrong AAD
        with self.assertRaises(AuthenticationError):
            etm.decrypt(ciphertext, wrong_aad)
        
        print("✓ Encrypt-then-MAC AAD tamper detection passed")
    
    def test_encrypt_then_mac_ciphertext_tamper(self):
        """Encrypt-then-MAC should detect ciphertext tampering."""
        key = os.urandom(16)
        plaintext = b"Test message"
        aad = b"aad"
        
        aes = AES(key)
        ctr = CTR(aes, os.urandom(16))
        etm = EncryptThenMAC(ctr)
        
        # Encrypt
        ciphertext = etm.encrypt(plaintext, aad)
        
        # Tamper with ciphertext
        tampered = bytearray(ciphertext)
        tampered[10] ^= 0x01
        
        # Try to decrypt
        with self.assertRaises(AuthenticationError):
            etm.decrypt(bytes(tampered), aad)
        
        print("✓ Encrypt-then-MAC ciphertext tamper detection passed")
    
    def test_encrypt_then_mac_empty_aad(self):
        """Encrypt-then-MAC with empty AAD."""
        key = os.urandom(16)
        plaintext = b"Message without AAD"
        aad = b""
        
        aes = AES(key)
        ctr = CTR(aes, os.urandom(16))
        etm = EncryptThenMAC(ctr)
        
        # Encrypt
        ciphertext = etm.encrypt(plaintext, aad)
        
        # Decrypt
        decrypted = etm.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ Encrypt-then-MAC with empty AAD passed")
    
    def test_encrypt_then_mac_different_keys(self):
        """Encrypt-then-MAC with different encryption and MAC keys."""
        enc_key = os.urandom(16)
        mac_key = os.urandom(32)  # HMAC can use longer keys
        
        plaintext = b"Message with separate keys"
        aad = b"aad"
        
        aes = AES(enc_key)
        ctr = CTR(aes, os.urandom(16))
        etm = EncryptThenMAC(ctr, hmac_key=mac_key, encryption_key=enc_key)
        
        # Encrypt
        ciphertext = etm.encrypt(plaintext, aad)
        
        # Decrypt
        decrypted = etm.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ Encrypt-then-MAC with separate keys passed")


if __name__ == "__main__":
    print("Running Encrypt-then-MAC tests...")
    print("=" * 60)
    
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("Encrypt-then-MAC tests completed!")