#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление оставшихся синтаксических ошибок в тестах
"""

def fix_file(filepath, fixes):
    """Исправить файл с несколькими исправлениями"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in fixes:
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Исправлен: {filepath}")
        return True
    
    return False

def main():
    """Основная функция"""
    
    # Исправления для test_interop.py
    interop_fixes = [
        ("print('   ✓ УСПЕХ: CryptoCore правильно расшифровал\")", 
         "print('   ✓ УСПЕХ: CryptoCore правильно расшифровал')"),
    ]
    
    # Исправления для test_modes.py
    modes_fixes = [
        ("print(f'  ✓ УСПЕХ\")", 
         "print(f'  ✓ УСПЕХ')"),
    ]
    
    print("Исправление оставшихся синтаксических ошибок...")
    
    fix_file('tests/test_interop.py', interop_fixes)
    fix_file('tests/test_modes.py', modes_fixes)
    
    print("\n✅ Все файлы исправлены!")
    print("\nЗапустите тесты снова:")
    print("python -m pytest tests/ -v")

if __name__ == "__main__":
    main()