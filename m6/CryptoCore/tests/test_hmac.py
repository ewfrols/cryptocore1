import unittest
import os
import tempfile
import hashlib
import binascii
import hmac as hmac_lib  # Импортируем стандартный модуль hmac

from cryptocore.crypto.mac import HMAC

class TestHMAC(unittest.TestCase):
    """Тесты для реализации HMAC (Sprint 5)."""
    
    def test_rfc_4231_test_case_1(self):
        """RFC 4231 Test Case 1 - Basic test."""
        key = binascii.unhexlify('0b' * 20)  # 20 bytes of 0x0b
        data = b"Hi There"
        
        hmac = HMAC(key, 'sha256')
        result = hmac.compute_hex(data)
        
        # Expected result from RFC 4231
        expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"
        
        self.assertEqual(result, expected)
        print(f"✓ RFC 4231 Test Case 1 passed")
    
    def test_rfc_4231_test_case_2(self):
        """RFC 4231 Test Case 2 - Key shorter than block size."""
        key = b"Jefe"  # "Jefe"
        data = b"what do ya want for nothing?"
        
        hmac = HMAC(key, 'sha256')
        result = hmac.compute_hex(data)
        
        # Expected result from RFC 4231 - ИСПРАВЛЕННЫЙ!
        expected = "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"
        
        self.assertEqual(result, expected)
        print(f"✓ RFC 4231 Test Case 2 passed")
    
    def test_rfc_4231_test_case_3(self):
        """RFC 4231 Test Case 3 - Data length 50."""
        key = binascii.unhexlify('aa' * 20)  # 20 bytes of 0xaa
        # 50 bytes of 0xdd
        data = binascii.unhexlify('dd' * 50)
        
        hmac = HMAC(key, 'sha256')
        result = hmac.compute_hex(data)
        
        # Expected result from RFC 4231
        expected = "773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe"
        
        self.assertEqual(result, expected)
        print(f"✓ RFC 4231 Test Case 3 passed")
    
    def test_key_longer_than_block_size(self):
        """Test key longer than block size (should be hashed first)."""
        # Key longer than 64 bytes
        key = b"x" * 100
        
        data = b"test message"
        
        hmac = HMAC(key, 'sha256')
        result = hmac.compute_hex(data)
        
        # Compare with Python's hashlib HMAC
        expected = hmac_sha256_python(key, data)
        
        self.assertEqual(result, expected)
        print(f"✓ Key longer than block size test passed")
    
    def test_key_shorter_than_block_size(self):
        """Test key shorter than block size (should be padded with zeros)."""
        key = b"short"
        
        data = b"test message"
        
        hmac = HMAC(key, 'sha256')
        result = hmac.compute_hex(data)
        
        # Compare with Python's hashlib HMAC
        expected = hmac_sha256_python(key, data)
        
        self.assertEqual(result, expected)
        print(f"✓ Key shorter than block size test passed")
    
    def test_key_exactly_block_size(self):
        """Test key exactly block size (64 bytes)."""
        key = b"x" * 64
        
        data = b"test message"
        
        hmac = HMAC(key, 'sha256')
        result = hmac.compute_hex(data)
        
        # Compare with Python's hashlib HMAC
        expected = hmac_sha256_python(key, data)
        
        self.assertEqual(result, expected)
        print(f"✓ Key exactly block size test passed")
    
    def test_empty_message(self):
        """Test HMAC with empty message."""
        key = b"secret"
        
        hmac = HMAC(key, 'sha256')
        result = hmac.compute_hex(b"")
        
        # Compare with Python's hashlib HMAC
        expected = hmac_sha256_python(key, b"")
        
        self.assertEqual(result, expected)
        print(f"✓ Empty message test passed")
    
    def test_file_hmac(self):
        """Test HMAC computation for a file."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"This is a test file for HMAC computation.\n" * 10)
            temp_file = f.name
        
        try:
            key = b"secret-key-123"
            
            hmac = HMAC(key, 'sha256')
            result = hmac.compute_file_hex(temp_file)
            
            # Compare with manual computation
            with open(temp_file, 'rb') as f:
                file_data = f.read()
            
            expected = hmac_sha256_python(key, file_data)
            
            self.assertEqual(result, expected)
            print(f"✓ File HMAC test passed")
            
        finally:
            os.unlink(temp_file)
    
    def test_verification_success(self):
        """Test HMAC verification (success case)."""
        key = b"verification-key"
        data = b"message to verify"
        
        hmac = HMAC(key, 'sha256')
        computed = hmac.compute(data)
        
        # Verify should succeed
        self.assertTrue(hmac.verify(data, computed))
        print(f"✓ Verification success test passed")
    
    def test_verification_failure_tampered_data(self):
        """Test HMAC verification failure with tampered data."""
        key = b"verification-key"
        original_data = b"original message"
        tampered_data = b"tampered message"
        
        hmac = HMAC(key, 'sha256')
        original_hmac = hmac.compute(original_data)
        
        # Verify with tampered data should fail
        self.assertFalse(hmac.verify(tampered_data, original_hmac))
        print(f"✓ Verification failure (tampered data) test passed")
    
    def test_verification_failure_wrong_key(self):
        """Test HMAC verification failure with wrong key."""
        correct_key = b"correct-key"
        wrong_key = b"wrong-key"
        data = b"test message"
        
        # Compute with correct key
        hmac_correct = HMAC(correct_key, 'sha256')
        correct_hmac = hmac_correct.compute(data)
        
        # Try to verify with wrong key
        hmac_wrong = HMAC(wrong_key, 'sha256')
        self.assertFalse(hmac_wrong.verify(data, correct_hmac))
        print(f"✓ Verification failure (wrong key) test passed")
    
    def test_hex_key_string(self):
        """Test HMAC with hex string key."""
        hex_key = "00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"
        data = b"test data"
        
        hmac = HMAC(hex_key, 'sha256')
        result = hmac.compute_hex(data)
        
        # Compare with bytes key
        key_bytes = binascii.unhexlify(hex_key)
        hmac_bytes = HMAC(key_bytes, 'sha256')
        expected = hmac_bytes.compute_hex(data)
        
        self.assertEqual(result, expected)
        print(f"✓ Hex key string test passed")
    
    def test_large_file_chunk_processing(self):
        """Test HMAC for large file with chunk processing."""
        # Create a 2MB file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            # Write 2MB of data
            chunk = b"ABCD" * 256  # 1KB
            for _ in range(2048):  # 2048 * 1KB = 2MB
                f.write(chunk)
            temp_file = f.name
        
        try:
            key = b"large-file-key"
            
            hmac = HMAC(key, 'sha256')
            result = hmac.compute_file_hex(temp_file, chunk_size=4096)
            
            # Compare with hashlib (read whole file)
            with open(temp_file, 'rb') as f:
                file_data = f.read()
            
            expected = hmac_sha256_python(key, file_data)
            
            self.assertEqual(result, expected)
            print(f"✓ Large file chunk processing test passed")
            
        finally:
            os.unlink(temp_file)


def hmac_sha256_python(key, data):
    """Helper function to compute HMAC-SHA256 using Python's hashlib."""
    return hmac_lib.new(key, data, hashlib.sha256).hexdigest()


if __name__ == "__main__":
    print("Running HMAC tests...")
    print("=" * 60)
    
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("HMAC implementation tests completed!")