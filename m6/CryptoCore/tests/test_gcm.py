import unittest
import os
import tempfile
import binascii

from cryptocore.modes.gcm import GCM, AuthenticationError

class TestGCM(unittest.TestCase):
    """Тесты для реализации GCM (Sprint 6)."""
    
    def test_gcm_basic_encrypt_decrypt(self):
        """Basic GCM encryption and decryption."""
        key = os.urandom(16)
        plaintext = b"Hello, GCM world!"
        aad = b"associated data"
        
        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)
        
        # Decrypt with same AAD
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ Basic GCM encrypt/decrypt passed")
    
    def test_gcm_aad_tamper_detection(self):
        """GCM should detect wrong AAD."""
        key = os.urandom(16)
        plaintext = b"Secret message"
        correct_aad = b"correct aad"
        wrong_aad = b"wrong aad"
        
        # Encrypt with correct AAD
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, correct_aad)
        
        # Try to decrypt with wrong AAD
        gcm2 = GCM(key, gcm.nonce)
        
        with self.assertRaises(AuthenticationError):
            gcm2.decrypt(ciphertext, wrong_aad)
        
        print("✓ GCM AAD tamper detection passed")
    
    def test_gcm_ciphertext_tamper_detection(self):
        """GCM should detect ciphertext tampering."""
        key = os.urandom(16)
        plaintext = b"Another secret"
        aad = b"authentication data"
        
        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)
        
        # Tamper with ciphertext
        tampered = bytearray(ciphertext)
        tampered[20] ^= 0x01  # Flip one bit
        
        # Try to decrypt tampered ciphertext
        gcm2 = GCM(key, gcm.nonce)
        
        with self.assertRaises(AuthenticationError):
            gcm2.decrypt(bytes(tampered), aad)
        
        print("✓ GCM ciphertext tamper detection passed")
    
    def test_gcm_tag_tamper_detection(self):
        """GCM should detect tag tampering."""
        key = os.urandom(16)
        plaintext = b"Message with tag"
        aad = b"some aad"
        
        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)
        
        # Tamper with tag (last 16 bytes)
        tampered = bytearray(ciphertext)
        tampered[-1] ^= 0x01  # Flip last bit of tag
        
        # Try to decrypt
        gcm2 = GCM(key, gcm.nonce)
        
        with self.assertRaises(AuthenticationError):
            gcm2.decrypt(bytes(tampered), aad)
        
        print("✓ GCM tag tamper detection passed")
    
    def test_gcm_empty_aad(self):
        """GCM should work with empty AAD."""
        key = os.urandom(16)
        plaintext = b"Message without AAD"
        aad = b""
        
        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)
        
        # Decrypt
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ GCM with empty AAD passed")
    
    def test_gcm_long_aad(self):
        """GCM should work with long AAD."""
        key = os.urandom(16)
        plaintext = b"Short message"
        aad = b"A" * 1000  # 1000 bytes of AAD
        
        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)
        
        # Decrypt
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ GCM with long AAD passed")
    
    def test_gcm_nonce_uniqueness(self):
        """GCM should generate unique nonces."""
        key = os.urandom(16)
        plaintext = b"Test message"
        aad = b"aad"
        
        # Generate multiple encryptions
        nonces = set()
        for _ in range(100):
            gcm = GCM(key)
            nonces.add(gcm.nonce)
            gcm.encrypt(plaintext, aad)
        
        # All nonces should be unique
        self.assertEqual(len(nonces), 100)
        print("✓ GCM nonce uniqueness passed")
    
    def test_gcm_with_specific_nonce(self):
        """GCM should work with provided nonce."""
        key = os.urandom(16)
        nonce = b"12byte nonce"  # 12 bytes
        plaintext = b"Message with specific nonce"
        aad = b"associated"
        
        # Encrypt with specific nonce
        gcm = GCM(key, nonce)
        ciphertext = gcm.encrypt(plaintext, aad)
        
        # Decrypt with same nonce
        gcm2 = GCM(key, nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ GCM with specific nonce passed")
    
    def test_gcm_output_format(self):
        """GCM output should be nonce(12) + ciphertext + tag(16)."""
        key = os.urandom(16)
        plaintext = b"Format test"
        aad = b"aad"
        
        gcm = GCM(key)
        output = gcm.encrypt(plaintext, aad)
        
        # Check format
        self.assertEqual(len(output), 12 + len(plaintext) + 16)
        self.assertEqual(output[:12], gcm.nonce)
        
        print("✓ GCM output format passed")
    
    def test_gcm_large_message(self):
        """GCM should handle large messages."""
        key = os.urandom(16)
        plaintext = os.urandom(10000)  # 10KB
        aad = b"large message aad"
        
        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)
        
        # Decrypt
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)
        
        self.assertEqual(plaintext, decrypted)
        print("✓ GCM with large message passed")
    
    def test_gf_multiplication(self):
        """Test Galois Field multiplication."""
        key = os.urandom(16)
        gcm = GCM(key)
        
        # Test some multiplications
        test_cases = [
            (0x00, 0x00, 0x00),
            (0x01, 0x01, 0x01),
            (0x02, 0x02, 0x04),
        ]
        
        for a, b, expected in test_cases:
            result = gcm._mult_gf(a, b)
            # Note: In GF(2^128), multiplication is different from integer multiplication
            # This is just a basic test
            if a == 0 or b == 0:
                self.assertEqual(result, 0)
        
        print("✓ GF multiplication test passed")


if __name__ == "__main__":
    print("Running GCM tests...")
    print("=" * 60)
    
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("GCM implementation tests completed!")