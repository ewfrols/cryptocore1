#!/usr/bin/env python3
"""
Прямой запуск HMAC без установки
"""

import sys
import os

# Убедитесь, что мы в правильной директории
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Добавим все необходимые пути
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, 'cryptocore'))

# Теперь можем импортировать
from crypto.mac import HMAC
import binascii

print("HMAC Direct Test")
print("=" * 60)

# Простой тест
key = b"test-key"
data = b"Hello, HMAC!"

hmac = HMAC(key, 'sha256')
result = hmac.compute_hex(data)

print(f"Key: {key}")
print(f"Data: {data}")
print(f"HMAC-SHA256: {result}")

# Проверка верификации
assert hmac.verify(data, binascii.unhexlify(result))
print("✓ Self-verification passed")

print("\n✅ HMAC работает корректно!")