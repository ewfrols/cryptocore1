#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полный функциональный тест CryptoCore v0.6.0
"""

import os
import sys
import tempfile
import hashlib

# Добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_sha256():
    """Тест SHA-256"""
    print("🧪 Тест SHA-256...")
    
    try:
        from cryptocore.crypto.hash.sha256_final import SHA256
        
        # Тест 1: Пустая строка
        sha = SHA256()
        sha.update(b"")
        result1 = sha.hexdigest()
        expected1 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result1 == expected1, f"FAIL: {result1} != {expected1}"
        
        # Тест 2: "abc"
        sha = SHA256()
        sha.update(b"abc")
        result2 = sha.hexdigest()
        expected2 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        assert result2 == expected2, f"FAIL: {result2} != {expected2}"
        
        print("  ✓ SHA-256 тест пройден")
        return True
    except Exception as e:
        print(f"  ✗ Ошибка SHA-256: {e}")
        return False

def test_hmac():
    """Тест HMAC-SHA256"""
    print("🧪 Тест HMAC-SHA256...")
    
    try:
        from cryptocore.crypto.mac.hmac import HMAC
        
        # Тестовые векторы из RFC 4231
        key = b"\x0b" * 20
        data = b"Hi There"
        
        hmac = HMAC(key, hashalgorithm="sha256")
        hmac.update(data)
        result = hmac.hexdigest()
        expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"
        
        assert result == expected, f"FAIL: {result} != {expected}"
        
        print("  ✓ HMAC-SHA256 тест пройден")
        return True
    except Exception as e:
        print(f"  ✗ Ошибка HMAC: {e}")
        return False

def test_gcm():
    """Тест GCM режима"""
    print("🧪 Тест GCM...")
    
    try:
        from cryptocore.modes.gcm import GCM
        
        # Простой тест
        key = bytes.fromhex("00000000000000000000000000000000")
        nonce = bytes.fromhex("000000000000000000000000")
        plaintext = b"Hello, GCM!"
        aad = b"authenticated but not encrypted"
        
        # Шифрование
        gcm = GCM(key)
        ciphertext, tag = gcm.encrypt(nonce, plaintext, aad)
        
        # Дешифрование
        gcm2 = GCM(key)
        decrypted = gcm2.decrypt(nonce, ciphertext, tag, aad)
        
        assert decrypted == plaintext, "Дешифрование не совпадает"
        
        print("  ✓ GCM тест пройден")
        return True
    except Exception as e:
        print(f"  ✗ Ошибка GCM: {e}")
        return False

def test_cli_commands():
    """Тест CLI команд"""
    print("🧪 Тест CLI команд...")
    
    try:
        import subprocess
        
        # Создаем тестовый файл
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"Test data for CLI\n" * 10)
            test_file = f.name
        
        # Тест 1: SHA-256 через CLI
        result = subprocess.run(
            [sys.executable, "-m", "cryptocore.main", "dgst", "--algorithm", "sha256", "--input", test_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✓ CLI SHA-256 работает")
            cli_ok = True
        else:
            print(f"  ✗ CLI SHA-256 ошибка: {result.stderr}")
            cli_ok = False
        
        # Очистка
        os.unlink(test_file)
        
        return cli_ok
    except Exception as e:
        print(f"  ✗ Ошибка CLI: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("=" * 60)
    print("CRYPTOCORE v0.6.0 - ПОЛНЫЙ ФУНКЦИОНАЛЬНЫЙ ТЕСТ")
    print("=" * 60)
    
    tests = [
        ("SHA-256", test_sha256),
        ("HMAC-SHA256", test_hmac),
        ("GCM", test_gcm),
        ("CLI", test_cli_commands),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"  ✗ Исключение: {e}")
            results.append((name, False))
    
    # Вывод результатов
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print("=" * 60)
    
    all_passed = True
    for name, success in results:
        status = "✓ ПРОЙДЕН" if success else "✗ НЕ ПРОЙДЕН"
        print(f"{name:20} {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! 🎉")
    else:
        print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)