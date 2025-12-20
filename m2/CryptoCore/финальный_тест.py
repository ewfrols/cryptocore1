#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный тест CFB - напрямую вызывает вашу реализацию
"""
import os
import sys
import tempfile

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cryptocore.modes.cfb import CFBMode

def финальный_тест():
    """Тестирует CFB напрямую, минуя cryptocore_simple.py"""
    print("=" * 60)
    print("ФИНАЛЬНЫЙ ТЕСТ CFB (прямая реализация)")
    print("=" * 60)
    
    ключ = '000102030405060708090a0b0c0d0e0f'
    iv_hex = '00112233445566778899aabbccddeeff'
    iv = bytes.fromhex(iv_hex)
    
    # Тестовые данные (140 байт как в основном тесте)
    тестовые_данные = b"Test file for all AES modes\r\n" + \
                     b"Line 2: Testing encryption and decryption\r\n" + \
                     b"Line 3: ABCDEFGHIJKLMNOPQRSTUVWXYZ\r\n" + \
                     b"Line 4: 1234567890!@#$%^&*()\r\n" + \
                     b"End of test file."
    
    print(f"Длина тестовых данных: {len(тестовые_данные)} байт")
    print(f"Ключ: {ключ}")
    print(f"IV: {iv_hex}")
    
    # Создаем объект CFB
    cfb = CFBMode(ключ)
    
    print("\n1. ШИФРОВАНИЕ...")
    зашифрованные = cfb.зашифровать(тестовые_данные, iv)
    print(f"   Зашифровано: {len(зашифрованные)} байт")
    
    # Сохраняем в файл с IV в начале (как делает cryptocore_simple.py)
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.enc') as f:
        f.write(iv + зашифрованные)  # IV + данные
        имя_зашифрованного = f.name
    
    print(f"   Файл с IV: {len(iv) + len(зашифрованные)} байт")
    print(f"   Сохранен в: {имя_зашифрованного}")
    
    print("\n2. РАСШИФРОВКА...")
    # Читаем файл обратно
    with open(имя_зашифрованного, 'rb') as f:
        все_данные = f.read()
    
    # Извлекаем IV и данные
    iv_из_файла = все_данные[:16]
    данные_из_файла = все_данные[16:]
    
    print(f"   IV из файла: {iv_из_файла.hex()}")
    print(f"   Данные из файла: {len(данные_из_файла)} байт")
    
    # Расшифровываем
    расшифрованные = cfb.расшифровать(данные_из_файла, iv_из_файла)
    print(f"   Расшифровано: {len(расшифрованные)} байт")
    
    print("\n3. СРАВНЕНИЕ...")
    if тестовые_данные == расшифрованные:
        print("   ✓ УСПЕХ! CFB работает правильно!")
        print(f"   ✓ Все {len(тестовые_данные)} байт совпадают")
    else:
        print("   ✗ ОШИБКА! Данные не совпадают")
        
        # Найдем отличия
        ошибки = 0
        for i in range(min(len(тестовые_данные), len(расшифрованные))):
            if тестовые_данные[i] != расшифрованные[i]:
                ошибки += 1
                if ошибки == 1:  # Покажем только первую ошибку
                    print(f"   Первая ошибка на байте {i}:")
                    print(f"     Оригинал: 0x{тестовые_данные[i]:02x}")
                    print(f"     Результат: 0x{расшифрованные[i]:02x}")
        
        print(f"   Всего ошибок: {ошибки}")
    
    # Очистка
    os.unlink(имя_зашифрованного)
    
    print("\n" + "="*60)
    print("ВЫВОД:")
    if тестовые_данные == расшифрованные:
        print("✅ ВАША РЕАЛИЗАЦИЯ CFB РАБОТАЕТ ПРАВИЛЬНО!")
        print("   Проблема в cryptocore_simple.py или в тестовом скрипте")
    else:
        print("❌ ВАША РЕАЛИЗАЦИЯ CFB ИМЕЕТ ОШИБКУ")
        print("   Нужно исправлять cfb.py")
    
    return тестовые_данные == расшифрованные

if __name__ == "__main__":
    успех = финальный_тест()
    sys.exit(0 if успех else 1)