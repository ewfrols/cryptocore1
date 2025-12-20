#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Работа с файлами для Sprint 2
Добавлена поддержка IV в файлах
"""
import sys
import os


class РаботаСФайлами:
    """Чтение и запись файлов с поддержкой IV"""
    
    @staticmethod
    def прочитать_файл(путь_к_файлу: str) -> bytes:
        """
        Читает файл как бинарные данные
        Работает с любыми файлами: текст, картинки, и т.д.
        """
        try:
            with open(путь_к_файлу, 'rb') as файл:
                данные = файл.read()
            
            print(f"✓ Прочитан файл: {путь_к_файлу}")
            print(f"  Размер: {len(данные)} байт")
            return данные
            
        except FileNotFoundError:
            print(f"✗ Ошибка: Файл '{путь_к_файлу}' не найден!", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"✗ Ошибка: Нет прав для чтения файла '{путь_к_файлу}'", file=sys.stderr)
            sys.exit(1)
        except Exception as ошибка:
            print(f"✗ Ошибка при чтении файла '{путь_к_файлу}': {ошибка}", file=sys.stderr)
            sys.exit(1)
    
    @staticmethod
    def записать_файл(путь_к_файлу: str, данные: bytes) -> None:
        """
        Записывает бинарные данные в файл
        """
        try:
            # Создаем папку если её нет
            папка = os.path.dirname(путь_к_файлу)
            if папка and not os.path.exists(папка):
                os.makedirs(папка)
            
            with open(путь_к_файлу, 'wb') as файл:
                файл.write(данные)
            
            print(f"✓ Записан файл: {путь_к_файлу}")
            print(f"  Размер: {len(данные)} байт")
            
        except PermissionError:
            print(f"✗ Ошибка: Нет прав для записи в '{путь_к_файлу}'", file=sys.stderr)
            sys.exit(1)
        except Exception as ошибка:
            print(f"✗ Ошибка при записи файла '{путь_к_файлу}': {ошибка}", file=sys.stderr)
            sys.exit(1)
    
    @staticmethod
    def проверить_файл(путь_к_файлу: str) -> None:
        """Проверяет что файл существует и доступен для чтения"""
        if not os.path.exists(путь_к_файлу):
            print(f"✗ Ошибка: Файл '{путь_к_файлу}' не существует!", file=sys.stderr)
            sys.exit(1)
        
        if not os.access(путь_к_файлу, os.R_OK):
            print(f"✗ Ошибка: Нет прав на чтение файла '{путь_к_файлу}'", file=sys.stderr)
            sys.exit(1)
    
    @staticmethod
    def проверить_размер_файла(путь_к_файлу: str, минимальный_размер: int = 0) -> bool:
        """Проверяет что файл не меньше указанного размера"""
        try:
            размер = os.path.getsize(путь_к_файлу)
            if размер < минимальный_размер:
                print(f"✗ Ошибка: Файл '{путь_к_файлу}' слишком маленький ({размер} < {минимальный_размер} байт)", file=sys.stderr)
                return False
            return True
        except Exception:
            return False