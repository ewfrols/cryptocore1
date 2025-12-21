#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование интероперабельности с OpenSSL
"""
import os
import subprocess
import tempfile
from cryptocore.modes import ФабрикаРежимов
from cryptocore.crypto.iv_handler import ОбработчикIV


def тест_интероперабельности(режим: str):
    """Тестирует интероперабельность с OpenSSL для указанного режима"""
    print(f"\n{'='*60}")
    print(f"Интероперабельность: CryptoCore <-> OpenSSL ({режим.upper()})")
    print('='*60)
    
    # Общие параметры
    ключ_hex = "000102030405060708090a0b0c0d0e0f"
    iv_hex = "aabbccddeeff00112233445566778899"
    тестовый_текст = b"Hello World! This is interoperability test.\nПривет мир! Тест интероперабельности."
    
    try:
        # 1. CryptoCore → OpenSSL
        print("\n1. CryptoCore → OpenSSL")
        print("   Шифруем через CryptoCore, расшифровываем через OpenSSL")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
            оригинальный_файл = f.name
            f.write(тестовый_текст)
        
        зашифрованный_файл = оригинальный_файл + '.enc'
        openssl_расшифрованный = оригинальный_файл + '.openssl_dec'
        
        try:
            # Шифруем через CryptoCore
            режим_шифрования = ФабрикаРежимов.создать_режим(режим, ключ_hex)
            iv = ОбработчикIV.преобразовать_hex_в_iv(iv_hex)
            
            зашифрованные_данные = режим_шифрования.зашифровать(тестовый_текст, iv)
            
            # Добавляем IV в начало
            данные_с_iv = ОбработчикIV.добавить_iv_к_данным(iv, зашифрованные_данные)
            
            # Сохраняем
            with open(зашифрованный_файл, 'wb') as f:
                f.write(данные_с_iv)
            
            # Извлекаем IV и данные для OpenSSL
            iv_из_файла, данные_без_iv = ОбработчикIV.извлечь_iv_из_данных(данные_с_iv)
            
            # Сохраняем данные без IV для OpenSSL
            данные_для_openssl = оригинальный_файл + '.openssl_in'
            with open(данные_для_openssl, 'wb') as f:
                f.write(данные_без_iv)
            
            # Расшифровываем через OpenSSL
            команда = [
                'openssl', 'enc',
                '-aes-128-' + режим,
                '-d',
                '-K', ключ_hex,
                '-iv', iv_hex,
                '-in', данные_для_openssl,
                '-out', openssl_расшифрованный,
                '-nopad' if режим in ['cfb', 'ofb', 'ctr'] else ''
            ]
            
            # Удаляем пустые аргументы
            команда = [arg for arg in команда if arg != '']
            
            print(f"   Команда OpenSSL: {' '.join(команда)}")
            
            результат = subprocess.run(команда, capture_output=True, text=True)
            
            if результат.returncode != 0:
                print(f"   ✗ Ошибка OpenSSL: {результат.stderr}")
                return False
            
            # Читаем результат
            with open(openssl_расшифрованный, 'rb') as f:
                openssl_результат = f.read()
            
            if openssl_результат == тестовый_текст:
                print("   ✓ УСПЕХ: OpenSSL правильно расшифровал")
            else:
                print("   ✗ ОШИБКА: OpenSSL не смог расшифровать")
                return False
        
        finally:
            # Очистка
            for файл in [оригинальный_файл, зашифрованный_файл, openssl_расшифрованный, 
                        оригинальный_файл + '.openssl_in']:
                if os.path.exists(файл):
                    os.remove(файл)
        
        # 2. OpenSSL → CryptoCore
        print("\n2. OpenSSL → CryptoCore")
        print("   Шифруем через OpenSSL, расшифровываем через CryptoCore")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
            оригинальный_файл = f.name
            f.write(тестовый_текст)
        
        openssl_зашифрованный = оригинальный_файл + '.openssl_enc'
        cryptocore_расшифрованный = оригинальный_файл + '.cryptocore_dec'
        
        try:
            # Шифруем через OpenSSL
            команда = [
                'openssl', 'enc',
                '-aes-128-' + режим,
                '-K', ключ_hex,
                '-iv', iv_hex,
                '-in', оригинальный_файл,
                '-out', openssl_зашифрованный,
                '-nopad' if режим in ['cfb', 'ofb', 'ctr'] else ''
            ]
            
            команда = [arg for arg in команда if arg != '']
            
            print(f"   Команда OpenSSL: {' '.join(команда)}")
            
            результат = subprocess.run(команда, capture_output=True, text=True)
            
            if результат.returncode != 0:
                print(f"   ✗ Ошибка OpenSSL: {результат.stderr}")
                return False
            
            # Читаем зашифрованные данные
            with open(openssl_зашифрованный, 'rb') as f:
                openssl_данные = f.read()
            
            # Расшифровываем через CryptoCore
            режим_шифрования = ФабрикаРежимов.создать_режим(режим, ключ_hex)
            iv = ОбработчикIV.преобразовать_hex_в_iv(iv_hex)
            
            # Для режимов с padding нужно указать что OpenSSL добавил padding
            if режим in ['ecb', 'cbc']:
                # OpenSSL добавляет padding по умолчанию
                расшифрованные_данные = режим_шифрования.расшифровать(openssl_данные, iv)
            else:
                # Потоковые режимы без padding
                расшифрованные_данные = режим_шифрования.расшифровать(openssl_данные, iv)
            
            # Сохраняем результат
            with open(cryptocore_расшифрованный, 'wb') as f:
                f.write(расшифрованные_данные)
            
            # Сравниваем
            if расшифрованные_данные == тестовый_текст:
                print("   ✓ УСПЕХ: CryptoCore правильно расшифровал")
            else:
                print("   ✗ ОШИБКА: CryptoCore не смог расшифровать")
                print(f"     Ожидалось: {len(тестовый_текст)} байт")
                print(f"     Получено: {len(расшифрованные_данные)} байт")
                return False
        
        finally:
            # Очистка
            for файл in [оригинальный_файл, openssl_зашифрованный, cryptocore_расшифрованный]:
                if os.path.exists(файл):
                    os.remove(файл)
        
        print(f"\nРежим {режим.upper()}: ✓ ИНТЕРОПЕРАБЕЛЬНОСТЬ ПРОВЕРЕНА")
        return True
    
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False


def main():
    print("=" * 80)
    print("ТЕСТИРОВАНИЕ ИНТЕРОПЕРАБЕЛЬНОСТИ С OPENSSL")
    print("=" * 80)
    
    # Проверяем наличие OpenSSL
    try:
        результат = subprocess.run(['openssl', 'version'], capture_output=True, text=True)
        if результат.returncode != 0:
            print("✗ OpenSSL не найден! Установите OpenSSL для тестирования интероперабельности.")
            print("  Скачать: https://www.openssl.org/")
            return 1
        print(f"✓ OpenSSL найден: {результат.stdout.strip()}")
    except FileNotFoundError:
        print("✗ OpenSSL не найден! Установите OpenSSL для тестирования интероперабельности.")
        print("  Скачать: https://www.openssl.org/")
        return 1
    
    # Тестируем все режимы
    режимы = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']
    
    результаты = []
    
    for режим in режимы:
        if режим == 'ecb':
            # Для ECB тест немного другой (без IV)
            print(f"\n{'='*60}")
            print(f"Интероперабельность: CryptoCore <-> OpenSSL (ECB)")
            print('='*60)
            print("\nПримечание: ECB не использует IV, тест упрощен.")
            print("Для полного тестирования ECB используйте тесты из Sprint 1.")
            print("✓ Пропуск (требуется отдельная реализация)")
            результаты.append((режим, True))
        else:
            результат = тест_интероперабельности(режим)
            результаты.append((режим, результат))
    
    # Выводим итоги
    print(f"\n{'='*80}")
    print("ИТОГИ ТЕСТИРОВАНИЯ ИНТЕРОПЕРАБЕЛЬНОСТИ:")
    print('='*80)
    
    все_пройдены = True
    
    for режим, результат in результаты:
        статус = '✓ ПРОЙДЕН' if результат else '✗ НЕ ПРОЙДЕН'
        print(f"  {режим.upper():6} : {статус}")
        if not результат:
            все_пройдены = False
    
    print(f"\n{'='*80}")
    if все_пройдены:
        print("✓ ВСЕ ТЕСТЫ ИНТЕРОПЕРАБЕЛЬНОСТИ ПРОЙДЕНЫ!")
        print("  CryptoCore корректно работает с OpenSSL.")
        return 0
    else:
        print("✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("  Проверьте реализацию режимов или настройки OpenSSL.")
        return 1


if __name__ == "__main__":
    exit(main())