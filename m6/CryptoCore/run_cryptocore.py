#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправленный скрипт запуска CryptoCore с правильными импортами
"""

import os
import sys
import subprocess

def main():
    """Основная функция"""
    print("🔧 CryptoCore - Исправленный запуск")
    print("=" * 50)
    
    # Проверяем наличие основных файлов
    required_files = [
        'cryptocore/__init__.py',
        'cryptocore/main.py',
        'cryptocore/modes/__init__.py',
        'cryptocore/modes/base_mode.py',
        'cryptocore/modes/gcm.py',
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Не найден файл: {file}")
            return 1
    
    # Исправляем импорты если нужно
    print("📁 Проверка структуры проекта...")
    
    # Способ 1: Запуск через модуль (рекомендуется)
    print("\n🚀 Способ 1: Запуск через python -m")
    cmd = [sys.executable, "-m", "cryptocore.main"] + sys.argv[1:]
    print(f"Команда: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Способ 2: Запуск через обертку
    print("\n🚀 Способ 2: Запуск через обертку")
    if os.path.exists('cryptocore_simple.py'):
        cmd = [sys.executable, "cryptocore_simple.py"] + sys.argv[1:]
        print(f"Команда: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        return result.returncode
    
    return 1

if __name__ == "__main__":
    sys.exit(main())