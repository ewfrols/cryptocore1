import unittest
import os
import tempfile
import hashlib
from pathlib import Path

from cryptocore.crypto.hash import SHA256, SHA3_256
from cryptocore.file_io import compute_hash

class TestSHA256(unittest.TestCase):
    def setUp(self):
        self.sha256 = SHA256()
    
    def test_empty_string(self):
        """Test SHA-256 of empty string."""
        self.sha256.update(b"")
        result = self.sha256.hexdigest()
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(result, expected)
    
    def test_abc(self):
        """Test SHA-256 of 'abc'."""
        self.sha256.update(b"abc")
        result = self.sha256.hexdigest()
        expected = "ba7816bf8f61cfea41414d6e5dae2223b00361a396177a9cb410ff61f20015ad"
        self.assertEqual(result, expected)
    
    def test_long_string(self):
        """Test SHA-256 of a longer string."""
        test_string = "abcdbcdecdefdefgefghfghjhjhjjhjjkjjkljklmklmnlmmmmpmppq"
        self.sha256.update(test_string.encode('utf-8'))
        result = self.sha256.hexdigest()
        expected = "248d6a6d620638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
        self.assertEqual(result, expected)
    
    def test_file_hashing(self):
        """Test hashing a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content for hashing\n")
            temp_file = f.name
        
        try:
            hash1 = self.sha256.hash_file(temp_file)
            
            # Compare with hashlib
            with open(temp_file, 'rb') as f:
                expected = hashlib.sha256(f.read()).hexdigest()
            
            self.assertEqual(hash1, expected)
        finally:
            os.unlink(temp_file)

class TestSHA3_256(unittest.TestCase):
    def test_basic(self):
        """Test SHA3-256 basic functionality."""
        sha3 = SHA3_256()
        sha3.update(b"test")
        result = sha3.hexdigest()
        
        # Compare with hashlib
        expected = hashlib.sha3_256(b"test").hexdigest()
        self.assertEqual(result, expected)
    
    def test_file_hashing(self):
        """Test SHA3-256 file hashing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Another test file\n")
            temp_file = f.name
        
        try:
            sha3 = SHA3_256()
            hash1 = sha3.hash_file(temp_file)
            
            # Compare with hashlib
            with open(temp_file, 'rb') as f:
                expected = hashlib.sha3_256(f.read()).hexdigest()
            
            self.assertEqual(hash1, expected)
        finally:
            os.unlink(temp_file)

class TestComputeHash(unittest.TestCase):
    def test_compute_hash_function(self):
        """Test the compute_hash utility function."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test file\n")
            temp_file = f.name
        
        try:
            # Test SHA-256
            hash1 = compute_hash(temp_file, 'sha256')
            with open(temp_file, 'rb') as f:
                expected1 = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(hash1, expected1)
            
            # Test SHA3-256
            hash2 = compute_hash(temp_file, 'sha3-256')
            with open(temp_file, 'rb') as f:
                expected2 = hashlib.sha3_256(f.read()).hexdigest()
            self.assertEqual(hash2, expected2)
        finally:
            os.unlink(temp_file)

if __name__ == "__main__":
    unittest.main()