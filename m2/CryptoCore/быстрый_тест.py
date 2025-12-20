#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Самый простой тест
"""
import os

# 1. Создаем файл
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write('Hello CryptoCore Sprint 2!')

print("1. Создан файл test.txt")

# 2. Тестируем CBC
print("\n2. Тестируем CBC режим...")
os.system('python run.py --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input test.txt')

print("\n3. Расшифровываем CBC...")
os.system('python run.py --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input test.txt.enc')

# 3. Проверяем
print("\n4. Проверяем...")
with open('test.txt', 'rb') as f1, open('test.txt.enc.dec', 'rb') as f2:
    if f1.read() == f2.read():
        print("✓ УСПЕХ: CBC работает!")
    else:
        print("✗ ОШИБКА: CBC не работает!")

# 4. Очистка
print("\n5. Очистка...")
for f in ['test.txt', 'test.txt.enc', 'test.txt.enc.dec']:
    if os.path.exists(f):
        os.remove(f)

input("\nНажмите Enter для выхода...")