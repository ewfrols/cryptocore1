#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка структуры проекта - исправленная версия для Windows
"""
import os
import sys

def проверить_структуру():
    print("Проверка структуры CryptoCore (Windows версия)...")
    print("=" * 50)
    
    # Используем os.path.join для правильных путей в Windows
    текущая_папка = os.getcwd()
    print(f"Текущая папка: {текущая_папка}")
    
    # Проверяем основные папки
    обязательные_папки = [
        'cryptocore',
        os.path.join('cryptocore', 'modes'),
        os.path.join('cryptocore', 'crypto')
    ]
    
    for папка in обязательные_папки:
        полный_путь = os.path.join(текущая_папка, папка)
        if os.path.exists(полный_путь) and os.path.isdir(полный_путь):
            print(f"✓ Папка: {папка}")
        else:
            print(f"✗ Отсутствует папка: {папка}")
            print(f"  Полный путь: {полный_путь}")
            return False
    
    # Проверяем обязательные файлы в cryptocore/modes
    обязательные_файлы_modes = [
        os.path.join('cryptocore', 'modes', '__init__.py'),
        os.path.join('cryptocore', 'modes', 'base_mode.py'),
        os.path.join('cryptocore', 'modes', 'ecb.py'),
        os.path.join('cryptocore', 'modes', 'cbc.py'),
        os.path.join('cryptocore', 'modes', 'cfb.py'),
        os.path.join('cryptocore', 'modes', 'ofb.py'),
        os.path.join('cryptocore', 'modes', 'ctr.py'),
    ]
    
    print("\nПроверка файлов в modes/:")
    все_файлы_есть = True
    for файл in обязательные_файлы_modes:
        полный_путь = os.path.join(текущая_папка, файл)
        if os.path.exists(полный_путь):
            размер = os.path.getsize(полный_путь)
            print(f"  ✓ {файл} ({размер} байт)")
        else:
            print(f"  ✗ Отсутствует: {файл}")
            print(f"    Полный путь: {полный_путь}")
            все_файлы_есть = False
    
    if not все_файлы_есть:
        print("\nПоказываю что есть в папке modes:")
        папка_modes = os.path.join(текущая_папка, 'cryptocore', 'modes')
        if os.path.exists(папка_modes):
            for item in os.listdir(папка_modes):
                полный_путь = os.path.join(папка_modes, item)
                if os.path.isdir(полный_путь):
                    print(f"    [папка] {item}/")
                else:
                    print(f"    [файл]  {item}")
    
    # Проверяем cryptocore/crypto
    обязательные_файлы_crypto = [
        os.path.join('cryptocore', 'crypto', '__init__.py'),
        os.path.join('cryptocore', 'crypto', 'aes_core.py'),
        os.path.join('cryptocore', 'crypto', 'padding.py'),
        os.path.join('cryptocore', 'crypto', 'iv_handler.py'),
    ]
    
    print("\nПроверка файлов в crypto/:")
    for файл in обязательные_файлы_crypto:
        полный_путь = os.path.join(текущая_папка, файл)
        if os.path.exists(полный_путь):
            размер = os.path.getsize(полный_путь)
            print(f"  ✓ {файл} ({размер} байт)")
        else:
            print(f"  ✗ Отсутствует: {файл}")
            print(f"    Полный путь: {полный_путь}")
            все_файлы_есть = False
    
    # Проверяем основной файлы
    основные_файлы = [
        os.path.join('cryptocore', '__init__.py'),
        os.path.join('cryptocore', 'main.py'),
        os.path.join('cryptocore', 'cli_parser.py'),
        os.path.join('cryptocore', 'file_io.py'),
    ]
    
    print("\nПроверка основных файлов:")
    for файл in основные_файлы:
        полный_путь = os.path.join(текущая_папка, файл)
        if os.path.exists(полный_путь):
            размер = os.path.getsize(полный_путь)
            print(f"  ✓ {файл} ({размер} байт)")
        else:
            print(f"  ✗ Отсутствует: {файл}")
            print(f"    Полный путь: {полный_путь}")
            все_файлы_есть = False
    
    print("\n" + "=" * 50)
    if все_файлы_есть:
        print("✓ Структура проекта в порядке!")
        return True
    else:
        print("✗ Есть отсутствующие файлы!")
        return False

def показать_содержимое_папки(путь, отступ=0):
    """Рекурсивно показывает содержимое папки"""
    if not os.path.exists(путь):
        return
    
    префикс = "  " * отступ
    
    for item in sorted(os.listdir(путь)):
        полный_путь = os.path.join(путь, item)
        if os.path.isdir(полный_путь):
            print(f"{префикс}[папка] {item}/")
            показать_содержимое_папки(полный_путь, отступ + 1)
        else:
            размер = os.path.getsize(полный_путь)
            print(f"{префикс}[файл]  {item} ({размер} байт)")

def проверить_импорты():
    print("\nПроверка импортов...")
    print("=" * 50)
    
    # Добавляем текущую папку в sys.path
    текущая_папка = os.getcwd()
    sys.path.insert(0, текущая_папка)
    print(f"Добавлено в sys.path: {текущая_папка}")
    
    try:
        # Пробуем импортировать
        print("1. Импортируем из modes...")
        try:
            from cryptocore.modes import ФабрикаРежимов
            print("   ✓ ФабрикаРежимов импортирована")
        except ImportError as e:
            print(f"   ✗ Ошибка импорта ФабрикаРежимов: {e}")
            
            # Покажем что в модуле modes
            print("\n   Содержимое модуля modes:")
            модуль_path = os.path.join(текущая_папка, 'cryptocore', 'modes', '__init__.py')
            if os.path.exists(модуль_path):
                with open(модуль_path, 'r', encoding='utf-8') as f:
                    print(f"   --- начало файла ---")
                    for i, line in enumerate(f.readlines()[:10], 1):
                        print(f"   {i:2}: {line.rstrip()}")
                    print(f"   --- конец файла ---")
            return False
        
        print("2. Пробуем создать режим ECB...")
        try:
            режим = ФабрикаРежимов.создать_режим('ecb', '000102030405060708090a0b0c0d0e0f')
            print(f"   ✓ Режим ECB создан: {type(режим).__name__}")
        except Exception as e:
            print(f"   ✗ Ошибка создания режима: {e}")
            return False
        
        print("3. Импортируем остальное...")
        try:
            from cryptocore.crypto.aes_core import AESCore
            print("   ✓ AESCore импортирован")
        except ImportError as e:
            print(f"   ✗ Ошибка импорта AESCore: {e}")
            return False
        
        try:
            from cryptocore.crypto.iv_handler import ОбработчикIV
            print("   ✓ ОбработчикIV импортирован")
        except ImportError as e:
            print(f"   ✗ Ошибка импорта ОбработчикIV: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"✗ Другая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def простой_тест():
    """Простой тест работы"""
    print("\nПростой тест работы...")
    print("=" * 50)
    
    try:
        # Импортируем
        from cryptocore.modes import ФабрикаРежимов
        
        # Тест CBC
        print("Тестируем CBC режим...")
        режим = ФабрикаРежимов.создать_режим('cbc', '000102030405060708090a0b0c0d0e0f')
        
        # Тестовые данные - ИСПРАВЛЕНО: используем encode для русских символов
        данные = "Hello CryptoCore! Test русских слов.".encode('utf-8')
        
        # Импортируем ОбработчикIV
        from cryptocore.crypto.iv_handler import ОбработчикIV
        iv = ОбработчикIV.сгенерировать_iv()
        print(f"Сгенерирован IV: {iv.hex()}")
        
        # Шифруем
        зашифровано = режим.зашифровать(данные, iv)
        print(f"Зашифровано: {len(данные)} -> {len(зашифровано)} байт")
        
        # Расшифровываем
        расшифровано = режим.расшифровать(зашифровано, iv)
        print(f"Расшифровано: {len(зашифровано)} -> {len(расшифровано)} байт")
        
        # Проверяем
        if расшифровано == данные:
            print("✓ УСПЕХ: Данные совпадают!")
            # Декодируем для отображения
            текст = расшифровано.decode('utf-8', errors='ignore')
            print(f"Текст: {текст[:50]}...")
            return True
        else:
            print("✗ ОШИБКА: Данные не совпадают!")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка при тесте: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ПРОВЕРКА СТРУКТУРЫ CRYPTOCORE SPRINT 2 (Windows)")
    print("=" * 60)
    
    # Показываем полную структуру
    print("\nПолная структура проекта:")
    показать_содержимое_папки('.')
    
    структура_ок = проверить_структуру()
    
    if структура_ок:
        print("\n" + "=" * 60)
        print("Проверка импортов и тест работы...")
        print("=" * 60)
        
        импорты_ок = проверить_импорты()
        
        if импорты_ок:
            тест_ок = простой_тест()
            
            if тест_ок:
                print("\n" + "=" * 60)
                print("✓ ВСЁ В ПОРЯДКЕ! Проект готов к работе.")
                print("=" * 60)
            else:
                print("\n✗ Тест не пройден")
        else:
            print("\n✗ Проблемы с импортами")
    else:
        print("\n✗ Проблемы со структурой проекта")
    
    input("\nНажмите Enter для выхода...")