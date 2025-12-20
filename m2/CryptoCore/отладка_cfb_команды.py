#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Отладка команд cryptocore_simple.py для CFB
"""
import subprocess
import os
import sys

def отладить_команду(команда, описание):
    """Запускает команду и показывает детальный вывод"""
    print(f"\n{'='*60}")
    print(f"{описание}")
    print('='*60)
    print(f"Команда: {' '.join(команда)}")
    
    результат = subprocess.run(команда, capture_output=True, text=True)
    
    print(f"Код возврата: {результат.returncode}")
    print(f"\nSTDOUT:")
    print(результат.stdout if результат.stdout else "(пусто)")
    
    print(f"\nSTDERR:")
    print(результат.stderr if результат.stderr else "(пусто)")
    
    return результат.returncode, результат.stdout, результат.stderr

# Создаем тестовый файл
тестовый_файл = 'отладка_тест.txt'
with open(тестовый_файл, 'w') as f:
    f.write('A' * 32)  # 32 символа 'A' (больше 16 байт)

ключ = '000102030405060708090a0b0c0d0e0f'
iv = '00112233445566778899aabbccddeeff'

# 1. Шифруем с cryptocore_simple.py
команда_шифрования = [
    sys.executable, 'cryptocore_simple.py',
    '--algorithm', 'aes',
    '--mode', 'cfb',
    '--encrypt',
    '--key', ключ,
    '--iv', iv,
    '--input', тестовый_файл
]

отладить_команду(команда_шифрования, "1. ШИФРОВАНИЕ CFB через cryptocore_simple.py")

# 2. Проверяем размер зашифрованного файла
зашифрованный = тестовый_файл + '.enc'
if os.path.exists(зашифрованный):
    размер = os.path.getsize(зашифрованный)
    print(f"\nРазмер зашифрованного файла: {размер} байт")
    
    # Покажем первые 64 байта в hex
    with open(зашифрованный, 'rb') as f:
        данные = f.read(64)
        print(f"Первые 64 байта зашифрованного файла (hex):")
        print(данные.hex())
        
        # Проверим, есть ли IV в начале файла
        if данные[:16].hex() == iv:
            print(f"\n✓ IV находится в начале файла: {данные[:16].hex()}")
            print(f"  Реальные данные начинаются с байта 16")
        else:
            print(f"\n⚠ IV НЕ в начале файла!")
            print(f"  Начало файла: {данные[:16].hex()}")
            print(f"  Ожидаемый IV: {iv}")

# 3. Расшифровываем
команда_расшифровки = [
    sys.executable, 'cryptocore_simple.py',
    '--algorithm', 'aes',
    '--mode', 'cfb',
    '--decrypt',
    '--key', ключ,
    '--iv', iv,
    '--input', зашифрованный
]

отладить_команду(команда_расшифровки, "2. РАСШИФРОВКА CFB через cryptocore_simple.py")

# 4. Сравниваем файлы
расшифрованный = зашифрованный + '.dec'
if os.path.exists(расшифрованный) and os.path.exists(тестовый_файл):
    with open(тестовый_файл, 'rb') as f1, open(расшифрованный, 'rb') as f2:
        оригинал = f1.read()
        результат = f2.read()
    
    print(f"\n{'='*60}")
    print("3. СРАВНЕНИЕ ФАЙЛОВ")
    print('='*60)
    
    if оригинал == результат:
        print("✓ Файлы идентичны!")
    else:
        print("✗ Файлы РАЗНЫЕ!")
        print(f"  Оригинал: {len(оригинал)} байт")
        print(f"  Результат: {len(результат)} байт")
        
        for i in range(min(len(оригинал), len(результат))):
            if оригинал[i] != результат[i]:
                print(f"  Первое отличие на байте {i}:")
                print(f"    Оригинал: 0x{оригинал[i]:02x} ({chr(оригинал[i]) if 32 <= оригинал[i] <= 126 else 'непечатный'})")
                print(f"    Результат: 0x{результат[i]:02x} ({chr(результат[i]) if 32 <= результат[i] <= 126 else 'непечатный'})")
                break

# 5. Очистка
for файл in [тестовый_файл, зашифрованный, расшифрованный]:
    if os.path.exists(файл):
        os.remove(файл)