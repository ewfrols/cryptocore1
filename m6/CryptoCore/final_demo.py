#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRYPTOCORE SPRINT 6 - ФИНАЛЬНАЯ ДЕМОНСТРАЦИЯ
Тестируем ВСЕ функции: SHA-256, HMAC, GCM
"""

import os
import sys
import tempfile
import subprocess

def print_section(title):
    """Печать секции"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def test_sha256_cli():
    """Тест SHA-256 через CLI"""
    print_section("ТЕСТ 1: SHA-256 ХЭШИРОВАНИЕ")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        f.write("Hello, CryptoCore! This is a test message.\n")
        f.write("Привет, CryptoCore! Это тестовое сообщение.\n")
        test_file = f.name
    
    print(f"Тестовый файл: {test_file}")
    
    # SHA-256
    print("\n[1] Вычисляем SHA-256...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--input", test_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ SHA-256 успешно вычислен")
        # Извлекаем хэш из вывода
        for line in result.stdout.split('\n'):
            if "Хэш:" in line:
                hash_value = line.split(":")[1].strip()
                print(f"   SHA-256: {hash_value}")
    else:
        print(f"❌ Ошибка SHA-256: {result.stderr}")
        return False
    
    # SHA3-256
    print("\n[2] Вычисляем SHA3-256...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha3-256", "--input", test_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ SHA3-256 успешно вычислен")
        for line in result.stdout.split('\n'):
            if "Хэш:" in line:
                hash_value = line.split(":")[1].strip()
                print(f"   SHA3-256: {hash_value}")
    else:
        print(f"❌ Ошибка SHA3-256: {result.stderr}")
        return False
    
    os.unlink(test_file)
    return True

def test_hmac_cli():
    """Тест HMAC через CLI"""
    print_section("ТЕСТ 2: HMAC-SHA256")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        f.write("Secret message for HMAC testing\n" * 3)
        test_file = f.name
    
    print(f"Тестовый файл: {test_file}")
    hmac_file = test_file + ".hmac"
    
    # Генерация HMAC
    print("\n[1] Генерация HMAC...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--hmac",
         "--key", "00112233445566778899aabbccddeeff", "--input", test_file, "--output", hmac_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ HMAC успешно сгенерирован")
        # Читаем сгенерированный HMAC
        with open(hmac_file, 'r') as f:
            hmac_value = f.read().strip()
            print(f"   HMAC: {hmac_value}")
    else:
        print(f"❌ Ошибка генерации HMAC: {result.stderr}")
        return False
    
    # Проверка HMAC
    print("\n[2] Проверка HMAC...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--hmac",
         "--key", "00112233445566778899aabbccddeeff", "--input", test_file, "--verify", hmac_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ HMAC проверка пройдена")
    else:
        print(f"❌ Ошибка проверки HMAC: {result.stderr}")
        return False
    
    # Проверка с неправильным ключом (должна завершиться с ошибкой)
    print("\n[3] Проверка с неправильным ключом (должна завершиться с ошибкой)...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--hmac",
         "--key", "deadbeefdeadbeefdeadbeefdeadbeef", "--input", test_file, "--verify", hmac_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("✅ Правильно обнаружен неверный ключ")
    else:
        print("❌ Ошибка: неправильный ключ должен вызывать ошибку")
        return False
    
    os.unlink(test_file)
    os.unlink(hmac_file)
    return True

def test_gcm_cli():
    """Тест GCM через CLI"""
    print_section("ТЕСТ 3: GCM ШИФРОВАНИЕ/ДЕШИФРОВАНИЕ")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        f.write("Очень секретное сообщение для GCM тестирования!\n")
        f.write("Этот текст должен быть полностью зашифрован и затем восстановлен.\n")
        f.write("Аутентификация данных гарантирует, что сообщение не было изменено.\n")
        test_file = f.name
    
    print(f"Тестовый файл: {test_file}")
    enc_file = test_file + ".enc"
    dec_file = test_file + ".dec"
    
    # Шифрование с текстовым AAD
    print("\n[1] Шифрование GCM с текстовым AAD...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "gcm", "--encrypt",
         "--key", "00112233445566778899aabbccddeeff",
         "--aad", "Test Authentication Data",
         "--input", test_file,
         "--output", enc_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ GCM шифрование успешно")
        for line in result.stdout.split('\n'):
            if "Nonce:" in line:
                print(f"   {line}")
            elif "Tag:" in line:
                print(f"   {line}")
    else:
        print(f"❌ Ошибка шифрования GCM: {result.stderr}")
        return False
    
    # Дешифрование
    print("\n[2] Дешифрование GCM...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "gcm", "--decrypt",
         "--key", "00112233445566778899aabbccddeeff",
         "--aad", "Test Authentication Data",
         "--input", enc_file,
         "--output", dec_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ GCM дешифрование успешно")
    else:
        print(f"❌ Ошибка дешифрования GCM: {result.stderr}")
        return False
    
    # Проверка, что файлы идентичны
    print("\n[3] Проверка целостности данных...")
    with open(test_file, 'rb') as f1, open(dec_file, 'rb') as f2:
        original = f1.read()
        decrypted = f2.read()
        
        if original == decrypted:
            print("✅ Данные полностью восстановлены, целостность сохранена")
        else:
            print("❌ Ошибка: данные не совпадают после шифрования/дешифрования")
            return False
    
    # Тест с неправильным AAD (должна быть ошибка аутентификации)
    print("\n[4] Тест с неправильным AAD (должна быть ошибка аутентификации)...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "gcm", "--decrypt",
         "--key", "00112233445566778899aabbccddeeff",
         "--aad", "Wrong Authentication Data",
         "--input", enc_file,
         "--output", test_file + ".wrong"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("✅ Правильно обнаружена ошибка аутентификации при неверном AAD")
    else:
        print("❌ Ошибка: неверный AAD должен вызывать ошибку аутентификации")
        return False
    
    # Очистка
    os.unlink(test_file)
    os.unlink(enc_file)
    os.unlink(dec_file)
    if os.path.exists(test_file + ".wrong"):
        os.unlink(test_file + ".wrong")
    
    return True

def test_comprehensive():
    """Комплексный тест"""
    print_section("ТЕСТ 4: КОМПЛЕКСНЫЙ СЦЕНАРИЙ")
    
    print("Сценарий: Шифруем файл, вычисляем HMAC для проверки целостности")
    
    # Создаем тестовые файлы
    original_file = "test_secret.txt"
    encrypted_file = "test_secret.enc"
    decrypted_file = "test_secret.dec"
    hmac_file = "test_secret.hmac"
    
    # Создаем секретный файл
    secret_content = """КОНФИДЕНЦИАЛЬНО
Дата: 2024-01-15
От: Агент 007
Кому: Центр

Сообщение:
Операция "Феникс" выполнена успешно.
Все документы уничтожены.
Встреча назначена на завтра в 14:00 у фонтана.

Кодовое слово: ОРХИДЕЯ
Конец сообщения."""
    
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(secret_content)
    
    print(f"\n1. Создан секретный файл: {original_file}")
    print(f"   Размер: {os.path.getsize(original_file)} байт")
    
    # 1. Вычисляем HMAC оригинального файла
    print("\n2. Вычисляем HMAC оригинального файла...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--hmac",
         "--key", "supersecretkey1234567890abcdef",
         "--input", original_file,
         "--output", hmac_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        with open(hmac_file, 'r') as f:
            original_hmac = f.read().strip()
        print(f"   HMAC оригинального файла: {original_hmac[:32]}...")
    else:
        print(f"❌ Ошибка вычисления HMAC: {result.stderr}")
        return False
    
    # 2. Шифруем файл
    print("\n3. Шифруем файл с помощью GCM...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "gcm", "--encrypt",
         "--key", "00112233445566778899aabbccddeeff",
         "--aad", "Операция Феникс 2024",
         "--input", original_file,
         "--output", encrypted_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"   Файл зашифрован: {encrypted_file}")
        print(f"   Размер зашифрованного: {os.path.getsize(encrypted_file)} байт")
    else:
        print(f"❌ Ошибка шифрования: {result.stderr}")
        return False
    
    # 3. Дешифруем файл
    print("\n4. Дешифруем файл...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "gcm", "--decrypt",
         "--key", "00112233445566778899aabbccddeeff",
         "--aad", "Операция Феникс 2024",
         "--input", encrypted_file,
         "--output", decrypted_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   Файл успешно дешифрован")
    else:
        print(f"❌ Ошибка дешифрования: {result.stderr}")
        return False
    
    # 4. Проверяем HMAC дешифрованного файла
    print("\n5. Проверяем целостность дешифрованного файла...")
    result = subprocess.run(
        [sys.executable, "cryptocore_simple.py", "dgst", "--algorithm", "sha256", "--hmac",
         "--key", "supersecretkey1234567890abcdef",
         "--input", decrypted_file,
         "--verify", hmac_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Целостность файла подтверждена!")
    else:
        print(f"❌ Ошибка: целостность файла нарушена!")
        return False
    
    # 5. Показываем, что файлы идентичны
    print("\n6. Сравнение оригинального и дешифрованного файлов...")
    with open(original_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
        if f1.read() == f2.read():
            print("✅ Файлы полностью идентичны!")
        else:
            print("❌ Файлы различаются!")
            return False
    
    # Очистка
    for file in [original_file, encrypted_file, decrypted_file, hmac_file]:
        if os.path.exists(file):
            os.unlink(file)
    
    return True

def main():
    """Основная функция"""
    print("\n" + "=" * 70)
    print(" CRYPTOCORE SPRINT 6 - ФИНАЛЬНАЯ ДЕМОНСТРАЦИЯ")
    print("=" * 70)
    print(" Тестирование всех компонентов проекта")
    print("=" * 70)
    
    print("\n📋 Обзор тестов:")
    print("1. SHA-256/SHA3-256 хэширование")
    print("2. HMAC-SHA256 генерация и проверка")
    print("3. GCM шифрование с аутентификацией")
    print("4. Комплексный сценарий безопасности")
    
    tests = [
        ("SHA-256 хэширование", test_sha256_cli),
        ("HMAC-SHA256", test_hmac_cli),
        ("GCM шифрование", test_gcm_cli),
        ("Комплексный сценарий", test_comprehensive),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n▶ Запуск: {name}")
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Исключение: {e}")
            results.append((name, False))
    
    # Итоги
    print("\n" + "=" * 70)
    print(" ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ НЕ ПРОЙДЕН"
        print(f"{name:25} {status}")
    
    print("\n" + "=" * 70)
    print(f" РЕЗУЛЬТАТ: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("\n🎉 ПОЗДРАВЛЯЕМ! CRYPTOCORE SPRINT 6 ПОЛНОСТЬЮ ФУНКЦИОНАЛЕН!")
        print("\nВсе криптографические функции работают корректно:")
        print("  • SHA-256/SHA3-256 хэширование")
        print("  • HMAC-SHA256 аутентификация")
        print("  • GCM аутентифицированное шифрование")
        print("  • Обнаружение изменений данных")
        print("  • Поддержка AAD (дополнительные аутентифицированные данные)")
        
        print("\n📚 Использование:")
        print("  python cryptocore_simple.py dgst --algorithm sha256 --input file.txt")
        print("  python cryptocore_simple.py dgst --algorithm sha256 --hmac --key KEY --input file.txt")
        print("  python cryptocore_simple.py gcm --encrypt --key HEX_KEY --aad DATA --input file.txt")
        print("  python cryptocore_simple.py gcm --decrypt --key HEX_KEY --aad DATA --input file.enc")
    else:
        print(f"\n⚠ Пройдено только {passed} из {total} тестов")
    
    print("=" * 70)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)