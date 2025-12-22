import unittest
import os
import tempfile
import hashlib

from cryptocore.crypto.hash import SHA256

class TestSHA256Correct(unittest.TestCase):
    """Тесты с ПРАВИЛЬНЫМИ тестовыми векторами."""
    
    def setUp(self):
        self.sha256 = SHA256()
    
    def test_empty_string(self):
        """SHA-256 пустой строки."""
        self.sha256.update(b"")
        result = self.sha256.hexdigest()
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(result, expected)
        # Проверим с hashlib
        self.assertEqual(result, hashlib.sha256(b"").hexdigest())
    
    def test_abc(self):
        """SHA-256 строки 'abc' - ПРАВИЛЬНЫЙ вектор."""
        self.sha256.update(b"abc")
        result = self.sha256.hexdigest()
        # ПРАВИЛЬНОЕ значение
        expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        self.assertEqual(result, expected)
        # Проверим с hashlib
        self.assertEqual(result, hashlib.sha256(b"abc").hexdigest())
    
    def test_hello(self):
        """SHA-256 строки 'hello'."""
        self.sha256.update(b"hello")
        result = self.sha256.hexdigest()
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertEqual(result, expected)
        self.assertEqual(result, hashlib.sha256(b"hello").hexdigest())
    
    def test_quick_brown_fox(self):
        """SHA-256 известной фразы."""
        text = "The quick brown fox jumps over the lazy dog"
        self.sha256.update(text.encode())
        result = self.sha256.hexdigest()
        expected = "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
        self.assertEqual(result, expected)
        self.assertEqual(result, hashlib.sha256(text.encode()).hexdigest())
    
    def test_nist_vector(self):
        """NIST тестовый вектор."""
        text = "abcdbcdecdefdefgefghfghihijhijkijkljklmklmnlmnomnopnopq"
        self.sha256.update(text.encode())
        result = self.sha256.hexdigest()
        # ПРАВИЛЬНОЕ значение (совпадает с hashlib)
        expected = "4250a961c45df449636b9e839b20ad18275437a6fe7712bd42b5603c101c2725"
        self.assertEqual(result, expected)
        # Проверим с hashlib
        self.assertEqual(result, hashlib.sha256(text.encode()).hexdigest())
    def test_file_hashing(self):
        """Хэширование файла."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test content for hashing\nSecond line\n")
            temp_file = f.name
        
        try:
            # Наша реализация
            hash1 = self.sha256.hash_file(temp_file)
            
            # Hashlib для проверки
            hashlib_hash = hashlib.sha256()
            with open(temp_file, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    hashlib_hash.update(chunk)
            
            expected = hashlib_hash.hexdigest()
            self.assertEqual(hash1, expected)
            
        finally:
            os.unlink(temp_file)
    
    def test_chunked_hashing(self):
        """Хэширование по частям."""
        text = "Hello, world! This is a test."
        
        # Хэширование целиком
        sha1 = SHA256()
        sha1.update(text.encode())
        hash1 = sha1.hexdigest()
        
        # Хэширование по частям
        sha2 = SHA256()
        sha2.update("Hello, ")
        sha2.update("world! ")
        sha2.update("This is ")
        sha2.update("a test.")
        hash2 = sha2.hexdigest()
        
        # Hashlib для проверки
        hash3 = hashlib.sha256(text.encode()).hexdigest()
        
        self.assertEqual(hash1, hash2)
        self.assertEqual(hash1, hash3)
    
    def test_avalanche_effect(self):
        """Лавинный эффект - изменение одного бита меняет весь хэш."""
        data1 = b"Hello, world!"
        data2 = b"Hello, world?"  # Изменен последний символ
        
        sha1 = SHA256()
        sha1.update(data1)
        hash1 = sha1.hexdigest()
        
        sha2 = SHA256()
        sha2.update(data2)
        hash2 = sha2.hexdigest()
        
        # Преобразуем в бинарный вид
        bin1 = bin(int(hash1, 16))[2:].zfill(256)
        bin2 = bin(int(hash2, 16))[2:].zfill(256)
        
        # Подсчитаем различающиеся биты
        diff_bits = sum(1 for b1, b2 in zip(bin1, bin2) if b1 != b2)
        
        # Лавинный эффект: должно измениться примерно 50% битов
        self.assertGreater(diff_bits, 100)
        self.assertLess(diff_bits, 156)
        print(f"Лавинный эффект: изменилось {diff_bits}/256 битов (~{diff_bits/256*100:.1f}%)")

if __name__ == "__main__":
    unittest.main(verbosity=2)