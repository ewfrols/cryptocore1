#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обертка для запуска CryptoCore с исправленными импортами
"""
import os
import sys
import argparse

# Добавляем текущую папку в путь
current_dir = os.getcwd()
sys.path.insert(0, current_dir)

def main():
    """Главная функция обертки"""
    parser = argparse.ArgumentParser(description='CryptoCore Wrapper - исправленные импорты')
    
    # Копируем все аргументы из оригинального парсера
    parser.add_argument('--algorithm', required=True, choices=['aes'])
    parser.add_argument('--mode', required=True, choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'])
    parser.add_argument('--encrypt', action='store_true')
    parser.add_argument('--decrypt', action='store_true')
    parser.add_argument('--key', required=True)
    parser.add_argument('--iv', help='IV в hex (32 символа)')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("CRYPTOCORE WRAPPER - Запуск с исправленными импортами")
    print("=" * 60)
    
    # Динамически импортируем и запускаем основную программу
    try:
        # Загружаем модули напрямую чтобы избежать проблем с импортами
        import importlib.util
        
        # Загружаем main.py
        main_path = os.path.join(current_dir, 'cryptocore', 'main.py')
        spec = importlib.util.spec_from_file_location("cryptocore_main", main_path)
        main_module = importlib.util.module_from_spec(spec)
        
        # Устанавливаем sys.argv для main модуля
        import argparse as argparse_module
        sys.modules['argparse'] = argparse_module
        
        # Выполняем модуль
        spec.loader.exec_module(main_module)
        
        print("✓ Модули загружены успешно")
        print(f"Режим: {args.mode.upper()}")
        print(f"Операция: {'ШИФРОВАНИЕ' if args.encrypt else 'РАСШИФРОВКА'}")
        print(f"Файл: {args.input}")
        
        # Имитируем вызов main() с аргументами
        # main_module.main() будет вызвана автоматически при импорте
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        print("\nЗапускаем упрощенную версию...")
        
        # Запускаем упрощенную версию как fallback
        import subprocess
        cmd = [
            sys.executable, 'cryptocore_simple.py',
            '--algorithm', args.algorithm,
            '--mode', args.mode,
            '--encrypt' if args.encrypt else '--decrypt',
            '--key', args.key,
            '--input', args.input,
        ]
        
        if args.iv:
            cmd.extend(['--iv', args.iv])
        if args.output:
            cmd.extend(['--output', args.output])
        
        subprocess.run(cmd)

if __name__ == "__main__":
    main()