#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование всех режимов CryptoCore - РАБОЧАЯ версия
"""
import os
import subprocess
import sys
import shutil
import tempfile

def создать_тестовый_файл(директория):
    """Создает тестовый файл в указанной директории"""
    путь = os.path.join(директория, 'test.txt')
    with open(путь, 'w', encoding='utf-8') as f:
        f.write('Test file for all AES modes\n')
        f.write('Line 2: Testing encryption\n')
        f.write('Line 3: Русский текст тоже работает!\n')
        f.write('Line 4: End of file\n')
    return путь

def запустить_команду_в_директории(команда, директория):
    """Запускает команду в указанной директории"""
    try:
        результат = subprocess.run(команда, capture_output=True, cwd=директория)
        return результат.returncode, результат.stdout, результат.stderr
    except Exception as e:
        return 1, b'', str(e).encode()

def тестировать_режим(режим, базовая_директория):
    """Тестирует один режим шифрования в отдельной директории"""
    print(f"\n{'='*50}")
    print(f"ТЕСТИРУЕМ РЕЖИМ: {режим.upper()}")
    print('='*50)
    
    # Создаем уникальную директорию для этого режима
    рабочая_директория = os.path.join(базовая_директория, f'тест_{режим}')
    os.makedirs(рабочая_директория, exist_ok=True)
    
    ключ = '000102030405060708090a0b0c0d0e0f'
    iv = '00112233445566778899aabbccddeeff'
    
    # Создаем тестовый файл
    тестовый_файл = создать_тестовый_файл(рабочая_директория)
    имя_файла = 'test.txt'
    
    # 1. Шифрование
    print(f"1. Шифрование ({режим})...")
    команда = [
        sys.executable, os.path.abspath('cryptocore_simple.py'),
        '--algorithm', 'aes',
        '--mode', режим,
        '--encrypt',
        '--key', ключ,
        '--input', имя_файла
    ]
    
    # Добавляем IV для режимов, которые его требуют
    if режим in ['cbc', 'cfb', 'ofb']:
        команда.extend(['--iv', iv])
    
    код_возврата, вывод, ошибка = запустить_команду_в_директории(команда, рабочая_директория)
    
    if код_возврата != 0:
        print(f"   ✗ Ошибка шифрования (код {код_возврата})")
        if ошибка:
            try:
                print(f"   Ошибка: {ошибка.decode('utf-8', errors='ignore')[:150]}")
            except:
                pass
        return False
    
    зашифрованный = os.path.join(рабочая_директория, 'test.txt.enc')
    if not os.path.exists(зашифрованный):
        print(f"   ✗ Зашифрованный файл не создан")
        return False
    
    print(f"   ✓ Зашифровано успешно")
    размер_зашифрованного = os.path.getsize(зашифрованный)
    print(f"   Размер зашифрованного файла: {размер_зашифрованного} байт")
    
    # 2. Расшифровка
    print(f"2. Расшифровка ({режим})...")
    команда = [
        sys.executable, os.path.abspath('cryptocore_simple.py'),
        '--algorithm', 'aes',
        '--mode', режим,
        '--decrypt',
        '--key', ключ,
        '--input', 'test.txt.enc'
    ]
    
    # ТОЧНО ТАКОЙ ЖЕ IV при расшифровке
    if режим in ['cbc', 'cfb', 'ofb']:
        команда.extend(['--iv', iv])
    
    код_возврата, вывод, ошибка = запустить_команду_в_директории(команда, рабочая_директория)
    
    if код_возврата != 0:
        print(f"   ✗ Ошибка расшифровки (код {код_возврата})")
        if ошибка:
            try:
                print(f"   Ошибка: {ошибка.decode('utf-8', errors='ignore')[:150]}")
            except:
                pass
        return False
    
    расшифрованный = os.path.join(рабочая_директория, 'test.txt.enc.dec')
    if not os.path.exists(расшифрованный):
        print(f"   ✗ Расшифрованный файл не создан")
        return False
    
    print(f"   ✓ Расшифровано успешно")
    
    # 3. Проверка совпадения
    print(f"3. Проверка совпадения файлов...")
    with open(тестовый_файл, 'rb') as f1, open(расшифрованный, 'rb') as f2:
        оригинал = f1.read()
        результат = f2.read()
    
    if оригинал == результат:
        print(f"   ✓ Файлы идентичны! Режим {режим.upper()} работает правильно.")
        print(f"   Размеры: оригинал={len(оригинал)}, зашифрованный={размер_зашифрованного}, расшифрованный={len(результат)}")
        успех = True
    else:
        print(f"   ✗ Файлы РАЗНЫЕ! Режим {режим.upper()} не работает.")
        print(f"     Оригинал: {len(оригинал)} байт")
        print(f"     Результат: {len(результат)} байт")
        
        # Найдем первое отличие
        for i in range(min(len(оригинал), len(результат))):
            if оригинал[i] != результат[i]:
                print(f"     Первое отличие на байте {i}: 0x{оригинал[i]:02x} vs 0x{результат[i]:02x}")
                break
        
        успех = False
    
    # 4. Очистка директории
    try:
        shutil.rmtree(рабочая_директория)
        print(f"   ✓ Очистка рабочей директории")
    except:
        pass
    
    return успех

def простой_тест_вручную(базовая_директория):
    """Простейший тест вручную в отдельных директориях"""
    print("\n" + "="*60)
    print("ПРОСТОЙ РУЧНОЙ ТЕСТ")
    print("="*60)
    
    результаты = []
    
    for режим in ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']:
        # Создаем уникальную директорию
        рабочая_директория = os.path.join(базовая_директория, f'простой_{режим}')
        os.makedirs(рабочая_директория, exist_ok=True)
        
        print(f"\nТестируем {режим.upper()}...")
        
        # Создаем тестовый файл
        тестовый_файл = os.path.join(рабочая_директория, 'test.bin')
        with open(тестовый_файл, 'wb') as f:
            f.write(b'ABCDEFGHIJKLMNOP')  # 16 байт
        
        ключ = '000102030405060708090a0b0c0d0e0f'
        iv = '00112233445566778899aabbccddeeff'
        
        try:
            # Шифруем
            команда = [
                sys.executable, os.path.abspath('cryptocore_simple.py'),
                '--algorithm', 'aes', '--mode', режим, 
                '--encrypt', '--key', ключ, '--input', 'test.bin'
            ]
            
            if режим in ['cbc', 'cfb', 'ofb']:
                команда.extend(['--iv', iv])
            
            результат = subprocess.run(команда, capture_output=True, cwd=рабочая_директория)
            
            if результат.returncode != 0 or not os.path.exists(os.path.join(рабочая_директория, 'test.bin.enc')):
                print(f"  ✗ Ошибка шифрования")
                if результат.stderr:
                    print(f"    {результат.stderr.decode('utf-8', errors='ignore')[:100]}")
                результаты.append((режим, False))
                continue
            
            # Расшифровываем
            команда = [
                sys.executable, os.path.abspath('cryptocore_simple.py'),
                '--algorithm', 'aes', '--mode', режим,
                '--decrypt', '--key', ключ, '--input', 'test.bin.enc'
            ]
            
            if режим in ['cbc', 'cfb', 'ofb']:
                команда.extend(['--iv', iv])
            
            результат = subprocess.run(команда, capture_output=True, cwd=рабочая_директория)
            
            if результат.returncode != 0 or not os.path.exists(os.path.join(рабочая_директория, 'test.bin.enc.dec')):
                print(f"  ✗ Ошибка расшифровки")
                if результат.stderr:
                    print(f"    {результат.stderr.decode('utf-8', errors='ignore')[:100]}")
                результаты.append((режим, False))
                continue
            
            # Сравниваем
            оригинал = os.path.join(рабочая_директория, 'test.bin')
            расшифрованный = os.path.join(рабочая_директория, 'test.bin.enc.dec')
            
            with open(оригинал, 'rb') as f1, open(расшифрованный, 'rb') as f2:
                if f1.read() == f2.read():
                    print(f"  ✓ {режим.upper()} работает!")
                    результаты.append((режим, True))
                else:
                    print(f"  ✗ {режим.upper()} не работает")
                    результаты.append((режим, False))
            
        except Exception as e:
            print(f"  ✗ Исключение: {e}")
            результаты.append((режим, False))
        
        # Очистка директории
        try:
            shutil.rmtree(рабочая_директория)
        except:
            pass
    
    return результаты

def main():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ВСЕХ РЕЖИМОВ CRYPTOCORE (ИСПРАВЛЕННАЯ ВЕРСИЯ)")
    print("=" * 60)
    
    # Создаем временную директорию для всех тестов
    with tempfile.TemporaryDirectory() as базовая_директория:
        print(f"Базовая директория тестов: {базовая_директория}")
        
        # Вариант 1: Простой тест
        print("\nВАРИАНТ 1: Простой тест с 16-байтным файлом")
        результаты = простой_тест_вручную(базовая_директория)
        
        # Вариант 2: Тест с текстовым файлом
        print("\n\nВАРИАНТ 2: Тест с текстовым файлом")
        
        # Тестируем только те режимы, которые прошли простой тест
        рабочие_режимы = [режим for режим, успех in результаты if успех]
        
        if рабочие_режимы:
            print(f"Тестируем рабочие режимы: {', '.join(рабочие_режимы)}")
            
            for режим in рабочие_режимы:
                успех = тестировать_режим(режим, базовая_директория)
                # Обновляем результат
                for i, (р, у) in enumerate(результаты):
                    if р == режим:
                        результаты[i] = (р, успех)
                        break
        
        # Выводим итоги
        print(f"\n{'='*60}")
        print("ИТОГИ ТЕСТИРОВАНИЯ:")
        print('='*60)
        
        работающих = sum(1 for _, успех in результаты if успех)
        всего = len(результаты)
        
        for режим, успех in результаты:
            статус = '✓ РАБОТАЕТ' if успех else '✗ НЕ РАБОТАЕТ'
            print(f"  {режим.upper():5} : {статус}")
        
        print(f"\nВсего режимов: {всего}")
        print(f"Работающих: {работающих}")
        print(f"Не работающих: {всего - работающих}")
        
        if работающих == всего:
            print("\n✓ ПОЗДРАВЛЯЮ! ВСЕ 5 РЕЖИМОВ РАБОТАЮТ!")
        elif работающих >= 3:
            print(f"\n✓ ХОРОШО! {работающих} из {всего} режимов работают.")
        else:
            print(f"\n✗ ТРЕБУЕТСЯ ДОРАБОТКА")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()