#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой запуск CryptoCore
"""
import sys
import os

# Добавляем текущую папку в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from cryptocore.main import main
    print("=" * 60)
    print("CryptoCore Sprint 2 - Запуск...")
    print("=" * 60)
    main()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("\nПроверь:")
    print("1. Папка 'cryptocore' есть в текущей папке")
    print("2. Внутри 'cryptocore' есть папки 'modes' и 'crypto'")
    print("3. Установлен pycryptodome: pip install pycryptodome")
    
    print(f"\nТекущая папка: {os.getcwd()}")
    print("Содержимое:")
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(f"  [папка] {item}/")
            # Покажем содержимое cryptocore если есть
            if item == 'cryptocore':
                try:
                    for sub in os.listdir('cryptocore'):
                        print(f"    - {sub}")
                except:
                    pass
        else:
            print(f"  [файл]  {item}")
    
    input("\nНажми Enter для выхода...")