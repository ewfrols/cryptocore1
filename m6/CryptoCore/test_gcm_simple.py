#!/usr/bin/env python3
"""
Простой тест GCM без установки пакета
"""

import sys
import os

# Добавить путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("ПРОСТОЙ ТЕСТ GCM (SPRINT 6)")
print("=" * 70)

# Попробуем импортировать GCM
try:
    from cryptocore.modes.gcm import GCM, AuthenticationError
    print("✓ GCM импортирован успешно")
except ImportError as e:
    print(f"✗ Ошибка импорта GCM: {e}")
    print("Проверьте, что файл cryptocore/modes/gcm.py существует")
    sys.exit(1)

import binascii

print("\n1. Базовый тест шифрования/дешифрования:")
key = os.urandom(16)
plaintext = b"Hello, GCM world!"
aad = b"associated data"

# Encrypt
gcm = GCM(key)
ciphertext = gcm.encrypt(plaintext, aad)

print(f"   Ключ: {key.hex()[:32]}...")
print(f"   Nonce: {gcm.nonce.hex()}")
print(f"   AAD: '{aad.decode()}'")
print(f"   Plaintext: '{plaintext.decode()}'")
print(f"   Длина ciphertext: {len(ciphertext)} байт")

# Decrypt
gcm2 = GCM(key, gcm.nonce)
decrypted = gcm2.decrypt(ciphertext, aad)

if decrypted == plaintext:
    print("   ✓ Дешифрование успешно")
else:
    print("   ✗ Ошибка дешифрования")

print("\n2. Тест обнаружения неправильного AAD:")
wrong_aad = b"wrong aad"
try:
    gcm3 = GCM(key, gcm.nonce)
    gcm3.decrypt(ciphertext, wrong_aad)
    print("   ✗ Не должно было пройти с неправильным AAD!")
except AuthenticationError:
    print("   ✓ Корректно обнаружен неправильный AAD")

print("\n3. Тест обнаружения измененного ciphertext:")
tampered = bytearray(ciphertext)
tampered[20] ^= 0x01  # Изменяем один байт
try:
    gcm4 = GCM(key, gcm.nonce)
    gcm4.decrypt(bytes(tampered), aad)
    print("   ✗ Не должно было пройти с измененным ciphertext!")
except AuthenticationError:
    print("   ✓ Корректно обнаружено изменение ciphertext")

print("\n4. Тест с пустым AAD:")
plaintext2 = b"Message without AAD"
gcm5 = GCM(key)
ciphertext2 = gcm5.encrypt(plaintext2, b"")
gcm6 = GCM(key, gcm5.nonce)
decrypted2 = gcm6.decrypt(ciphertext2, b"")

if decrypted2 == plaintext2:
    print("   ✓ Работает с пустым AAD")
else:
    print("   ✗ Ошибка с пустым AAD")

print("\n5. Тест формата вывода:")
# Проверяем формат: nonce(12) + ciphertext + tag(16)
if len(ciphertext) == 12 + len(plaintext) + 16:
    print("   ✓ Формат вывода правильный")
    print(f"   Nonce: {ciphertext[:12].hex()}")
    print(f"   Ciphertext: {len(ciphertext[12:-16])} байт")
    print(f"   Tag: {ciphertext[-16:].hex()[:32]}...")
else:
    print(f"   ✗ Неправильный формат: ожидалось {12 + len(plaintext) + 16}, получили {len(ciphertext)}")

print("\n" + "=" * 70)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 70)