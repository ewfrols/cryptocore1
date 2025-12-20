#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер аргументов командной строки
"""
import argparse
import sys
import os


class ПарсерАргументов:
    """Разбирает аргументы командной строки"""
    
    @staticmethod
    def разобрать_аргументы():
        """Читает аргументы из командной строки"""
        parser = argparse.ArgumentParser(
            description='CryptoCore: Шифрование/расшифровка файлов AES-128 ECB',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False  # Добавим свою помощь
        )
        
        # Обязательные аргументы
        parser.add_argument(
            '--algorithm',
            type=str,
            required=True,
            choices=['aes'],
            help='Алгоритм шифрования (пока только aes)'
        )
        
        parser.add_argument(
            '--mode',
            type=str,
            required=True,
            choices=['ecb'],
            help='Режим работы (пока только ecb)'
        )
        
        # Операция (шифрование ИЛИ расшифровка)
        группа_операций = parser.add_mutually_exclusive_group(required=True)
        группа_операций.add_argument(
            '--encrypt',
            dest='operation',
            action='store_const',
            const='encrypt',
            help='Зашифровать файл'
        )
        группа_операций.add_argument(
            '--decrypt',
            dest='operation',
            action='store_const',
            const='decrypt',
            help='Расшифровать файл'
        )
        
        # Ключ
        parser.add_argument(
            '--key',
            type=str,
            required=True,
            help='Ключ шифрования (32 hex-символа, пример: 00112233445566778899aabbccddeeff)'
        )
        
        # Файлы
        parser.add_argument(
            '--input',
            type=str,
            required=True,
            help='Входной файл (что шифровать/расшифровывать)'
        )
        
        parser.add_argument(
            '--output',
            type=str,
            help='Выходной файл (необязательно - будет создан автоматически)'
        )
        
        # Добавим помощь
        parser.add_argument(
            '--help',
            action='help',
            help='Показать это сообщение и выйти'
        )
        
        args = parser.parse_args()
        
        # Проверяем ключ
        ПарсерАргументов.проверить_ключ(args.key)
        
        # Проверяем входной файл
        if not os.path.exists(args.input):
            print(f"Ошибка: Файл '{args.input}' не найден!", file=sys.stderr)
            sys.exit(1)
        
        # Создаем имя выходного файла если не указано
        if not args.output:
            args.output = ПарсерАргументов.создать_имя_файла(args.input, args.operation)
        
        return {
            'алгоритм': args.algorithm,
            'режим': args.mode,
            'операция': args.operation,
            'ключ': args.key,
            'вход': args.input,
            'выход': args.output
        }
    
    @staticmethod
    def проверить_ключ(ключ: str) -> None:
        """Проверяет что ключ правильный"""
        if not ключ:
            print("Ошибка: Ключ не может быть пустым", file=sys.stderr)
            sys.exit(1)
        
        # Проверяем что это hex-строка
        try:
            байты_ключа = bytes.fromhex(ключ)
        except ValueError:
            print(f"Ошибка: Ключ '{ключ}' - неверный hex-формат", file=sys.stderr)
            print("Ключ должен содержать только 0-9, a-f (32 символа)", file=sys.stderr)
            print("Пример: 000102030405060708090a0b0c0d0e0f", file=sys.stderr)
            sys.exit(1)
        
        # Проверяем длину (AES-128 = 16 байт = 32 hex-символа)
        if len(ключ) != 32:
            print(f"Ошибка: Ключ должен быть 32 символа, а не {len(ключ)}", file=sys.stderr)
            print("Пример правильного ключа: 000102030405060708090a0b0c0d0e0f", file=sys.stderr)
            sys.exit(1)
    
    @staticmethod
    def создать_имя_файла(входной_файл: str, операция: str) -> str:
        """Создает имя файла если пользователь не указал"""
        if операция == 'encrypt':
            # Шифрование: добавляем .enc
            return входной_файл + '.enc'
        else:
            # Расшифровка: убираем .enc или добавляем .dec
            if входной_файл.endswith('.enc'):
                return входной_файл[:-4] + '.dec'
            else:
                return входной_файл + '.dec'
    
    @staticmethod
    def показать_помощь():
        """Показывает как пользоваться программой"""
        print("Использование: cryptocore --algorithm aes --mode ecb [--encrypt|--decrypt]")
        print("                --key КЛЮЧ --input ВХОДНОЙ_ФАЙЛ [--output ВЫХОДНОЙ_ФАЙЛ]")
        print("\nПример шифрования:")
        print("  cryptocore --algorithm aes --mode ecb --encrypt \\")
        print("    --key 000102030405060708090a0b0c0d0e0f \\")
        print("    --input текст.txt --output зашифрованный.bin")
        print("\nПример с русскими именами файлов:")
        print("  cryptocore --algorithm aes --mode ecb --encrypt \\")
        print("    --key 00112233445566778899aabbccddeeff \\")
        print("    --input 'документ.txt' --output 'зашифрованный файл.bin'")