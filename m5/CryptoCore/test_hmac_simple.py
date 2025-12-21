#!/usr/bin/env python3
"""
Простой тест HMAC без установки пакета
"""

import sys
import os

# Добавить путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Попробуем импортировать наш HMAC
try:
    from cryptocore.crypto.mac import HMAC
    print("✓ Успешно импортирован HMAC из cryptocore")
except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    print("Попытка альтернативного импорта...")
    
    # Попробуем добавить пути вручную
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cryptocore'))
    sys.path.insert(0, os.path.dirname(__file__))
    
    try:
        from crypto.mac import HMAC
        print("✓ Успешно импортирован через альтернативный путь")
    except ImportError as e2:
        print(f"✗ Вторая ошибка импорта: {e2}")
        sys.exit(1)

import binascii
import hashlib
import hmac as hmac_lib

print("\n" + "=" * 70)
print("ТЕСТИРОВАНИЕ HMAC-SHA256")
print("=" * 70)

# Тест 1: RFC 4231 Test Case 1
print("\n1. Тест RFC 4231 Test Case 1:")
key = binascii.unhexlify('0b' * 20)
data = b"Hi There"

h = HMAC(key, 'sha256')
result = h.compute_hex(data)
expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"

print(f"   Ключ: {'0b' * 20}")
print(f"   Данные: 'Hi There'")
print(f"   Наш HMAC:    {result}")
print(f"   Ожидаемый:   {expected}")
print(f"   Совпадает:   {'✓' if result == expected else '✗'}")

# Сравнение с Python's hmac
py_hmac = hmac_lib.new(key, data, hashlib.sha256).hexdigest()
print(f"   Python hmac: {py_hmac}")
print(f"   Сравнение с Python: {'✓' if result == py_hmac else '✗'}")

# Тест 2: RFC 4231 Test Case 2
print("\n2. Тест RFC 4231 Test Case 2:")
key = b"Jefe"
data = b"what do ya want for nothing?"

h = HMAC(key, 'sha256')
result = h.compute_hex(data)
expected = "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"

print(f"   Ключ: 'Jefe'")
print(f"   Данные: 'what do ya want for nothing?'")
print(f"   Наш HMAC:    {result}")
print(f"   Ожидаемый:   {expected}")
print(f"   Совпадает:   {'✓' if result == expected else '✗'}")

py_hmac = hmac_lib.new(key, data, hashlib.sha256).hexdigest()
print(f"   Python hmac: {py_hmac}")
print(f"   Сравнение с Python: {'✓' if result == py_hmac else '✗'}")

# Тест 3: Пустое сообщение
print("\n3. Тест с пустым сообщением:")
key = b"secret"
data = b""

h = HMAC(key, 'sha256')
result = h.compute_hex(data)
py_hmac = hmac_lib.new(key, data, hashlib.sha256).hexdigest()

print(f"   Ключ: 'secret'")
print(f"   Данные: (пусто)")
print(f"   Наш HMAC:    {result}")
print(f"   Python hmac: {py_hmac}")
print(f"   Совпадает:   {'✓' if result == py_hmac else '✗'}")

# Тест 4: Ключ разной длины
print("\n4. Тест разных размеров ключей:")
test_cases = [
    ("Короткий (5 байт)", b"short"),
    ("Точный размер (64 байта)", b"x" * 64),
    ("Длинный (100 байт)", b"y" * 100),
]

all_pass = True
for name, key in test_cases:
    h = HMAC(key, 'sha256')
    our_result = h.compute_hex(b"test message")
    py_result = hmac_lib.new(key, b"test message", hashlib.sha256).hexdigest()
    
    if our_result == py_result:
        print(f"   {name}: ✓")
    else:
        print(f"   {name}: ✗ (наш: {our_result[:16]}..., Python: {py_result[:16]}...)")
        all_pass = False

# Тест 5: Hex ключ
print("\n5. Тест с hex строкой ключа:")
hex_key = "00112233445566778899aabbccddeeff"
h = HMAC(hex_key, 'sha256')
result = h.compute_hex(b"test")
key_bytes = binascii.unhexlify(hex_key)
h2 = HMAC(key_bytes, 'sha256')
expected = h2.compute_hex(b"test")

print(f"   Hex ключ: {hex_key}")
print(f"   Наш HMAC: {result}")
print(f"   Ожидаемый: {expected}")
print(f"   Совпадает: {'✓' if result == expected else '✗'}")

print("\n" + "=" * 70)
if all_pass:
    print("✅ ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
else:
    print("⚠️  НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
print("=" * 70)