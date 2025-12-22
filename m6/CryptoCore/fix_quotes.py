#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрое исправление незакрытых кавычек в тестовых файлах
"""

def fix_quotes():
    """Исправить незакрытые кавычки в файлах"""
    
    # Файл 1: test_interop.py
    with open('tests/test_interop.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Исправляем строку 86
    content = content.replace(
        "print('   ✓ УСПЕХ: OpenSSL правильно расшифровал\")",
        "print('   ✓ УСПЕХ: OpenSSL правильно расшифровал')"
    )
    
    with open('tests/test_interop.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Исправлен: tests/test_interop.py")
    
    # Файл 2: test_modes.py
    with open('tests/test_modes.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Исправляем строку 49
    content = content.replace(
        "print('  Пропуск: ECB не поддерживает пустые данные\")",
        "print('  Пропуск: ECB не поддерживает пустые данные')"
    )
    
    with open('tests/test_modes.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Исправлен: tests/test_modes.py")
    
    print("✅ Все файлы исправлены!")

if __name__ == "__main__":
    fix_quotes()