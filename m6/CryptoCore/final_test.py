#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ФИНАЛЬНЫЙ ТЕСТ CRYPTOCORE SPRINT 6
Проверка всех компонентов: SHA-256, HMAC, GCM
"""

import os
import sys
import tempfile
import subprocess

# Добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_header(text):
    """Печать заголовка"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def test_sha256():
    """Тест SHA-256"""
    print_header("ТЕСТ 1: SHA-256 ХЭШИРОВАНИЕ")
    
    try:
        from cryptocore.crypto.hash.sha256_final import SHA256
        
        # Тест 1: Пустая строка
        sha = SHA256()
        sha.update(b"")
        result = sha.hexdigest()
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        
        if result == expected:
            print("✅ Пустая строка: PASSED")
        else:
            print(f"❌ Пустая строка: FAILED")
            print(f"   Ожидалось: {expected}")
            print(f"   Получено:  {result}")
            return False
        
        # Тест 2: "abc"
        sha = SHA256()
        sha.update(b"abc")
        result = sha.hexdigest()
        expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        
        if result == expected:
            print("✅ Строка 'abc': PASSED")
        else:
            print(f"❌ Строка 'abc': FAILED")
            print(f"   Ожидалось: {expected}")
            print(f"   Получено:  {result}")
            return False
        
        print("✅ ВСЕ ТЕСТЫ SHA-256 ПРОЙДЕНЫ")
        return True
    
    except Exception as e:
        print(f"❌ Ошибка SHA-256: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_hmac():
    """Тест HMAC"""
    print_header("ТЕСТ 2: HMAC-SHA256")
    
    try:
        from cryptocore.crypto.mac.hmac import HMAC
        
        # Тест из RFC 4231
        key = b"\x0b" * 20
        data = b"Hi There"
        
        hmac = HMAC(key)
        hmac.update(data)
        result = hmac.hexdigest()
        expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"
        
        if result == expected:
            print("✅ RFC 4231 Test Case 1: PASSED")
        else:
            print(f"❌ RFC 4231 Test Case 1: FAILED")
            print(f"   Ожидалось: {expected}")
            print(f"   Получено:  {result}")
            return False
        
        # Тест с hex ключом
        key_hex = "00112233445566778899aabbccddeeff"
        data = b"Test message"
        
        hmac = HMAC(key_hex)
        hmac.update(data)
        result = hmac.hexdigest()
        
        # Проверка самосогласованности
        hmac2 = HMAC(key_hex)
        result2 = hmac2.compute_hex(data)
        
        if result == result2:
            print("✅ Самосогласованность HMAC: PASSED")
        else:
            print("❌ Самосогласованность HMAC: FAILED")
            return False
        
        print("✅ ВСЕ ТЕСТЫ HMAC ПРОЙДЕНЫ")
        return True
    
    except Exception as e:
        print(f"❌ Ошибка HMAC: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gcm():
    """Тест GCM"""
    print_header("ТЕСТ 3: GCM ШИФРОВАНИЕ")
    
    try:
        from cryptocore.modes.gcm import GCM
        
        # Простой тест
        key = bytes.fromhex("00000000000000000000000000000000")
        nonce = bytes.fromhex("000000000000000000000000")
        plaintext = b"Hello, GCM!"
        aad = b"authenticated data"
        
        # Шифрование
        gcm = GCM(key)
        ciphertext, tag = gcm.encrypt(nonce, plaintext, aad)
        
        # Дешифрование
        gcm2 = GCM(key)
        decrypted = gcm2.decrypt(nonce, ciphertext, tag, aad)
        
        if decrypted == plaintext:
            print("✅ Базовое шифрование/дешифрование: PASSED")
        else:
            print("❌ Базовое шифрование/дешифрование: FAILED")
            return False
        
        # Тест с разными ключами
        key2 = bytes.fromhex("00112233445566778899aabbccddeeff")
        gcm3 = GCM(key2)
        
        try:
            # Должна быть ошибка аутентификации
            gcm3.decrypt(nonce, ciphertext, tag, aad)
            print("❌ Обнаружение неверного ключа: FAILED (должна быть ошибка)")
            return False
        except:
            print("✅ Обнаружение неверного ключа: PASSED")
        
        print("✅ ВСЕ ТЕСТЫ GCM ПРОЙДЕНЫ")
        return True
    
    except Exception as e:
        print(f"❌ Ошибка GCM: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli():
    """Тест командной строки"""
    print_header("ТЕСТ 4: КОМАНДНАЯ СТРОКА")
    
    try:
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b"Test data for CLI testing\n" * 5)
            test_file = f.name
        
        print(f"Создан тестовый файл: {test_file}")
        
        # Тест 1: SHA-256 через CLI
        print("\n1. Тестируем SHA-256 через cryptocore_simple.py...")
        result = subprocess.run(
            [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--input", test_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ CLI SHA-256: PASSED")
        else:
            print(f"❌ CLI SHA-256: FAILED")
            print(f"Ошибка: {result.stderr}")
            return False
        
        # Тест 2: HMAC через CLI
        print("\n2. Тестируем HMAC через cryptocore_simple.py...")
        result = subprocess.run(
            [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--hmac", 
             "--key", "00112233445566778899aabbccddeeff", "--input", test_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ CLI HMAC: PASSED")
        else:
            print(f"❌ CLI HMAC: FAILED")
            print(f"Ошибка: {result.stderr}")
            return False
        
        # Тест 3: GCM через CLI
        print("\n3. Тестируем GCM через cryptocore_simple.py...")
        
        # Шифрование
        enc_result = subprocess.run(
            [sys.executable, "cryptocore_simple.py", "gcm", "--encrypt",
             "--key", "00112233445566778899aabbccddeeff",
             "--aad", "aabbcc",
             "--input", test_file,
             "--output", test_file + ".enc"],
            capture_output=True,
            text=True
        )
        
        if enc_result.returncode == 0:
            print("✅ CLI GCM шифрование: PASSED")
        else:
            print(f"❌ CLI GCM шифрование: FAILED")
            print(f"Ошибка: {enc_result.stderr}")
            return False
        
        # Дешифрование
        dec_result = subprocess.run(
            [sys.executable, "cryptocore_simple.py", "gcm", "--decrypt",
             "--key", "00112233445566778899aabbccddeeff",
             "--aad", "aabbcc",
             "--input", test_file + ".enc",
             "--output", test_file + ".dec"],
            capture_output=True,
            text=True
        )
        
        if dec_result.returncode == 0:
            print("✅ CLI GCM дешифрование: PASSED")
        else:
            print(f"❌ CLI GCM дешифрование: FAILED")
            print(f"Ошибка: {dec_result.stderr}")
            return False
        
        # Проверяем, что файлы идентичны
        with open(test_file, 'rb') as f1, open(test_file + '.dec', 'rb') as f2:
            if f1.read() == f2.read():
                print("✅ Файлы идентичны после шифрования/дешифрования: PASSED")
            else:
                print("❌ Файлы различаются после шифрования/дешифрования: FAILED")
                return False
        
        # Очистка
        os.unlink(test_file)
        os.unlink(test_file + '.enc')
        os.unlink(test_file + '.dec')
        
        print("✅ ВСЕ ТЕСТЫ КОМАНДНОЙ СТРОКИ ПРОЙДЕНЫ")
        return True
    
    except Exception as e:
        print(f"❌ Ошибка CLI: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция тестирования"""
    print("=" * 70)
    print("CRYPTOCORE SPRINT 6 - ФИНАЛЬНЫЙ ТЕСТ")
    print("=" * 70)
    print("Тестирование всех компонентов: SHA-256, HMAC, GCM, CLI")
    print("=" * 70)
    
    tests = [
        ("SHA-256", test_sha256),
        ("HMAC-SHA256", test_hmac),
        ("GCM", test_gcm),
        ("Командная строка", test_cli),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n▶ Запуск теста: {name}")
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Исключение в тесте {name}: {e}")
            results.append((name, False))
    
    # Вывод результатов
    print("\n" + "=" * 70)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 70)
    
    all_passed = True
    passed_count = 0
    
    for name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ НЕ ПРОЙДЕН"
        print(f"{name:20} {status}")
        if success:
            passed_count += 1
        else:
            all_passed = False
    
    print("\n" + "=" * 70)
    print(f"ПРОЙДЕНО: {passed_count}/{len(tests)}")
    
    if all_passed:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("CryptoCore Sprint 6 полностью функционален!")
        print("\nИспользование:")
        print("  python cryptocore_simple.py gcm --encrypt --key HEX_KEY --input file.txt")
        print("  python cryptocore_simple.py dgst --algorithm sha256 --hmac --key KEY --input file.txt")
    else:
        print("\n⚠ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
    
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)