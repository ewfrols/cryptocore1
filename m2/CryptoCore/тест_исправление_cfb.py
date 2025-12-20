#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест исправления CFB в cryptocore_simple.py
"""
import subprocess
import os
import sys

def создать_тестовый_файл(имя, размер=140):
    """Создает тестовый файл заданного размера"""
    данные = b'A' * размер
    with open(имя, 'wb') as f:
        f.write(данные)
    return имя

# Параметры теста
ключ = '000102030405060708090a0b0c0d0e0f'
iv = '00112233445566778899aabbccddeeff'
файл = 'тест_cfb.bin'

print("=" * 60)
print("ТЕСТ ИСПРАВЛЕНИЯ CFB В CRYPTOCORE_SIMPLE.PY")
print("=" * 60)

# 1. Создаем файл (140 байт как в основном тесте)
создать_тестовый_файл(файл, 140)
размер_оригинала = os.path.getsize(файл)
print(f"Создан файл: {файл} ({размер_оригинала} байт)")

# 2. Шифруем
print("\n1. ШИФРОВАНИЕ CFB...")
команда_шифрования = [
    sys.executable, 'cryptocore_simple.py',
    '--algorithm', 'aes',
    '--mode', 'cfb',
    '--encrypt',
    '--key', ключ,
    '--iv', iv,
    '--input', файл
]

результат = subprocess.run(команда_шифрования, capture_output=True, text=True)
print(f"   Код: {результат.returncode}")
if результат.stdout:
    print(f"   Вывод: {результат.stdout.strip()}")

зашифрованный = файл + '.enc'
if os.path.exists(зашифрованный):
    размер_зашифрованного = os.path.getsize(зашифрованный)
    print(f"   Создан файл: {зашифрованный} ({размер_зашифрованного} байт)")
else:
    print(f"   Ошибка: файл не создан")
    sys.exit(1)

# 3. Расшифровываем
print("\n2. РАСШИФРОВКА CFB...")
команда_расшифровки = [
    sys.executable, 'cryptocore_simple.py',
    '--algorithm', 'aes',
    '--mode', 'cfb',
    '--decrypt',
    '--key', ключ,
    '--iv', iv,
    '--input', зашифрованный
]

результат = subprocess.run(команда_расшифровки, capture_output=True, text=True)
print(f"   Код: {результат.returncode}")
if результат.stdout:
    print(f"   Вывод: {результат.stdout.strip()}")

расшифрованный = зашифрованный + '.dec'
if not os.path.exists(расшифрованный):
    print(f"   Ошибка: файл не создан")
    sys.exit(1)

# 4. Сравниваем
print("\n3. СРАВНЕНИЕ ФАЙЛОВ...")
with open(файл, 'rb') as f1, open(расшифрованный, 'rb') as f2:
    оригинал = f1.read()
    результат_расшифровки = f2.read()

if оригинал == результат_расшифровки:
    print(f"   ✓ УСПЕХ! Файлы идентичны")
    print(f"   ✓ CFB работает правильно")
else:
    print(f"   ✗ ОШИБКА! Файлы разные")
    print(f"     Оригинал: {len(оригинал)} байт")
    print(f"     Результат: {len(результат_расшифровки)} байт")
    
    # Найдем первое отличие
    for i in range(min(len(оригинал), len(результат_расшифровки))):
        if оригинал[i] != результат_расшифровки[i]:
            print(f"     Первое отличие на байте {i}:")
            print(f"       Оригинал: 0x{оригинал[i]:02x}")
            print(f"       Результат: 0x{результат_расшифровки[i]:02x}")
            break

# 5. Очистка
for f in [файл, зашифрованный, расшифрованный]:
    if os.path.exists(f):
        os.remove(f)

print("\n" + "="*60)
if оригинал == результат_расшифровки:
    print("ИСПРАВЛЕНИЕ РАБОТАЕТ! Теперь запустите основной тест.")
else:
    print("ИСПРАВЛЕНИЕ НЕ СРАБОТАЛО. Проверьте код.")