#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование всех режимов CryptoCore - исправленная версия
"""
import os
import subprocess
import sys

def создать_тестовый_файл():
    """Создает тестовый файл"""
    with open('test_all.txt', 'w', encoding='utf-8') as f:
        f.write('Test file for all AES modes\n')
        f.write('Line 2: Testing encryption\n')
        f.write('Line 3: Русский текст тоже работает!\n')
        f.write('Line 4: End of file\n')
    print("Создан тестовый файл: test_all.txt")
    return 'test_all.txt'

def запустить_команду(команда):
    """Запускает команду и возвращает результат"""
    try:
        # Используем binary mode для вывода чтобы избежать проблем с кодировкой
        результат = subprocess.run(команда, capture_output=True)
        return результат.returncode, результат.stdout, результат.stderr
    except Exception as e:
        return 1, b'', str(e).encode()

def тестировать_режим(режим):
    """Тестирует один режим шифрования с уникальными именами файлов"""
    print(f"\n{'='*50}")
    print(f"ТЕСТИРУЕМ РЕЖИМ: {режим.upper()}")
    print('='*50)
    
    ключ = '000102030405060708090a0b0c0d0e0f'
    iv = '00112233445566778899aabbccddeeff'
    тестовый_файл = 'test_all.txt'
    
    # УНИКАЛЬНЫЕ имена для каждого режима, чтобы не было конфликтов
    зашифрованный = f'test_{режим}.enc'
    расшифрованный = f'test_{режим}.dec'
    
    # 1. ОЧИСТКА: удаляем возможные остатки от предыдущих тестов
    for файл in [зашифрованный, расшифрованный, 
                 'test_all.txt.enc', 'test_all.txt.enc.dec',
                 f'test_all_{режим}.enc', f'test_all_{режим}.enc.dec']:
        if os.path.exists(файл):
            try:
                os.remove(файл)
            except:
                pass
    
    # 2. Шифрование
    print(f"1. Шифрование ({режим})...")
    
    # Собираем команду для шифрования
    команда_шифрования = [
        sys.executable, 'cryptocore_simple.py',
        '--algorithm', 'aes',
        '--mode', режим,
        '--encrypt',
        '--key', ключ,
        '--input', тестовый_файл
    ]
    
    # Для CFB, CBC, OFB добавляем IV
    if режим in ['cbc', 'cfb', 'ofb']:
        команда_шифрования.extend(['--iv', iv])
    
    код_возврата, вывод, ошибка = запустить_команду(команда_шифрования)
    
    # Показываем вывод
    if вывод:
        try:
            вывод_текст = вывод.decode('utf-8', errors='ignore').strip()
            if вывод_текст:
                print(f"   Вывод: {вывод_текст[:80]}")
        except:
            pass
    
    if код_возврата != 0:
        print(f"   ✗ Ошибка шифрования (код {код_возврата})")
        if ошибка:
            try:
                ошибка_текст = ошибка.decode('utf-8', errors='ignore').strip()
                if ошибка_текст:
                    print(f"   Ошибка: {ошибка_текст[:150]}")
            except:
                pass
        return False
    
    # Проверяем, что файл создан (стандартное имя)
    стандартный_зашифрованный = тестовый_файл + '.enc'
    if not os.path.exists(стандартный_зашифрованный):
        print(f"   ✗ Зашифрованный файл не создан")
        return False
    
    # Переименовываем стандартный файл в уникальный, чтобы не было конфликта
    if os.path.exists(стандартный_зашифрованный):
        try:
            os.rename(стандартный_зашифрованный, зашифрованный)
        except Exception as e:
            print(f"   ⚠ Не удалось переименовать файл: {e}")
            зашифрованный = стандартный_зашифрованный
    
    print(f"   ✓ Зашифровано успешно")
    размер_зашифрованного = os.path.getsize(зашифрованный)
    print(f"   Размер зашифрованного файла: {размер_зашифрованного} байт")
    
    # 3. Расшифровка
    print(f"2. Расшифровка ({режим})...")
    
    команда_расшифровки = [
        sys.executable, 'cryptocore_simple.py',
        '--algorithm', 'aes',
        '--mode', режим,
        '--decrypt',
        '--key', ключ,
        '--input', зашифрованный
    ]
    
    # ТОЧНО ТАКОЙ ЖЕ IV при расшифровке
    if режим in ['cbc', 'cfb', 'ofb']:
        команда_расшифровки.extend(['--iv', iv])
    
    код_возврата, вывод, ошибка = запустить_команду(команда_расшифровки)
    
    if код_возврата != 0:
        print(f"   ✗ Ошибка расшифровки (код {код_возврата})")
        if ошибка:
            try:
                ошибка_текст = ошибка.decode('utf-8', errors='ignore').strip()
                if ошибка_текст:
                    print(f"   Ошибка: {ошибка_текст[:150]}")
            except:
                pass
        
        # Удаляем временные файлы перед выходом
        for файл in [зашифрованный, расшифрованный]:
            if os.path.exists(файл):
                try:
                    os.remove(файл)
                except:
                    pass
        return False
    
    # Проверяем, что файл создан (стандартное имя)
    стандартный_расшифрованный = зашифрованный + '.dec'
    if not os.path.exists(стандартный_расшифрованный):
        print(f"   ✗ Расшифрованный файл не создан")
        # Удаляем временные файлы
        if os.path.exists(зашифрованный):
            try:
                os.remove(зашифрованный)
            except:
                pass
        return False
    
    # Переименовываем в уникальное имя
    if os.path.exists(стандартный_расшифрованный):
        try:
            os.rename(стандартный_расшифрованный, расшифрованный)
        except Exception as e:
            print(f"   ⚠ Не удалось переименовать файл: {e}")
            расшифрованный = стандартный_расшифрованный
    
    print(f"   ✓ Расшифровано успешно")
    
    # 4. Проверка совпадения
    print(f"3. Проверка совпадения файлов...")
    
    try:
        with open(тестовый_файл, 'rb') as f1, open(расшифрованный, 'rb') as f2:
            оригинал = f1.read()
            результат = f2.read()
        
        if оригинал == результат:
            print(f"   ✓ Файлы идентичны! Режим {режим.upper()} работает правильно.")
            
            размер_оригинала = len(оригинал)
            размер_расшифрованного = len(результат)
            
            print(f"   Размеры: оригинал={размер_оригинала}, зашифрованный={размер_зашифрованного}, расшифрованный={размер_расшифрованного}")
            
            успех = True
        else:
            print(f"   ✗ Файлы РАЗНЫЕ! Режим {режим.upper()} не работает.")
            print(f"     Оригинал: {len(оригинал)} байт")
            print(f"     Результат: {len(результат)} байт")
            
            # Найдем первое отличие
            for i in range(min(len(оригинал), len(результат))):
                if оригинал[i] != результат[i]:
                    print(f"     Первое отличие на байте {i}: 0x{оригинал[i]:02x} vs 0x{результат[i]:02x}")
                    # Покажем контекст
                    start = max(0, i - 10)
                    end = min(len(оригинал), i + 10)
                    print(f"     Контекст оригинала: {оригинал[start:end].hex()}")
                    print(f"     Контекст результата: {результат[start:end].hex()}")
                    break
            
            успех = False
            
    except Exception as e:
        print(f"   ✗ Ошибка при сравнении файлов: {e}")
        успех = False
    
    # 5. Очистка (ВСЕГДА удаляем временные файлы)
    print(f"4. Очистка временных файлов...")
    удалено = 0
    for файл in [зашифрованный, расшифрованный, 
                 тестовый_файл + '.enc', тестовый_файл + '.enc.dec',
                 f'test_{режим}.enc', f'test_{режим}.dec']:
        if os.path.exists(файл):
            try:
                os.remove(файл)
                удалено += 1
            except Exception as e:
                print(f"   ⚠ Не удалось удалить {файл}: {e}")
    
    if удалено > 0:
        print(f"   ✓ Удалено {удалено} временных файлов")
    
    return успех

def простой_тест_вручную():
    """Простейший тест вручную"""
    print("\n" + "="*60)
    print("ПРОСТОЙ РУЧНОЙ ТЕСТ")
    print("="*60)
    
    # Создаем очень простой файл
    тестовый_файл = 'test_simple.bin'
    with open(тестовый_файл, 'wb') as f:
        f.write(b'ABCDEFGHIJKLMNOP')  # Ровно 16 байт (один блок)
    
    ключ = '000102030405060708090a0b0c0d0e0f'
    iv = '00112233445566778899aabbccddeeff'
    результаты = []
    
    for режим in ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']:
        print(f"\nТестируем {режим.upper()}...")
        
        # Очистка перед каждым тестом
        for файл in ['test_simple.bin.enc', 'test_simple.bin.enc.dec',
                    f'test_simple_{режим}.enc', f'test_simple_{режим}.dec']:
            if os.path.exists(файл):
                try:
                    os.remove(файл)
                except:
                    pass
        
        try:
            # Шифруем
            команда = [sys.executable, 'cryptocore_simple.py', '--algorithm', 'aes', '--mode', режим, 
                      '--encrypt', '--key', ключ, '--input', тестовый_файл]
            
            if режим in ['cbc', 'cfb', 'ofb']:
                команда.extend(['--iv', iv])
            
            результат = subprocess.run(команда, capture_output=True)
            
            if результат.returncode != 0 or not os.path.exists('test_simple.bin.enc'):
                print(f"  ✗ Ошибка шифрования")
                if результат.stderr:
                    print(f"    {результат.stderr.decode('utf-8', errors='ignore')[:100]}")
                результаты.append((режим, False))
                continue
            
            # Расшифровываем
            команда = [sys.executable, 'cryptocore_simple.py', '--algorithm', 'aes', '--mode', режим,
                      '--decrypt', '--key', ключ, '--input', 'test_simple.bin.enc']
            
            if режим in ['cbc', 'cfb', 'ofb']:
                команда.extend(['--iv', iv])
            
            результат = subprocess.run(команда, capture_output=True)
            
            if результат.returncode != 0 or not os.path.exists('test_simple.bin.enc.dec'):
                print(f"  ✗ Ошибка расшифровки")
                if результат.stderr:
                    print(f"    {результат.stderr.decode('utf-8', errors='ignore')[:100]}")
                результаты.append((режим, False))
                continue
            
            # Сравниваем
            with open(тестовый_файл, 'rb') as f1, open('test_simple.bin.enc.dec', 'rb') as f2:
                if f1.read() == f2.read():
                    print(f"  ✓ {режим.upper()} работает!")
                    результаты.append((режим, True))
                else:
                    print(f"  ✗ {режим.upper()} не работает - файлы разные")
                    результаты.append((режим, False))
            
            # Очистка после теста
            for файл in ['test_simple.bin.enc', 'test_simple.bin.enc.dec']:
                if os.path.exists(файл):
                    try:
                        os.remove(файл)
                    except:
                        pass
                
        except Exception as e:
            print(f"  ✗ Исключение: {e}")
            результаты.append((режим, False))
    
    # Удаляем тестовый файл
    if os.path.exists(тестовый_файл):
        os.remove(тестовый_файл)
    
    return результаты

def main():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ВСЕХ РЕЖИМОВ CRYPTOCORE SPRINT 2")
    print("=" * 60)
    
    # Вариант 1: Простой тест с бинарным файлом
    print("\nВАРИАНТ 1: Простой тест с 16-байтным файлом")
    результаты = простой_тест_вручную()
    
    # Вариант 2: Тест с текстовым файлом (если простой тест работает)
    print("\n\nВАРИАНТ 2: Тест с текстовым файлом")
    try:
        тестовый_файл = создать_тестовый_файл()
        
        # Тестируем только те режимы, которые прошли простой тест
        рабочие_режимы = [режим for режим, успех in результаты if успех]
        
        if рабочие_режимы:
            print(f"\nТестируем рабочие режимы: {', '.join(рабочие_режимы)}")
            
            for режим in рабочие_режимы:
                успех = тестировать_режим(режим)
                # Обновляем результат
                for i, (р, у) in enumerate(результаты):
                    if р == режим:
                        результаты[i] = (р, успех)
                        break
        
        # Удаляем тестовый файл
        if os.path.exists(тестовый_файл):
            os.remove(тестовый_файл)
            
    except Exception as e:
        print(f"Ошибка при тесте с текстовым файлом: {e}")
    
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
    
    print(f"\n{'='*60}")
    if работающих == всего:
        print("✓ ПОЗДРАВЛЯЮ! ВСЕ 5 РЕЖИМОВ РАБОТАЮТ!")
        print("  Sprint 2 выполнен успешно!")
    elif работающих >= 3:
        print("✓ ХОРОШО! Большинство режимов работает.")
        print(f"  {работающих} из {всего} режимов работают.")
    else:
        print("✗ ТРЕБУЕТСЯ ДОРАБОТКА")
        print(f"  Только {работающих} из {всего} режимов работают.")
    
    print(f"\n{'='*60}")
    print("Использование:")
    print("  python cryptocore_simple.py --algorithm aes --mode MODE --encrypt --key KEY --input FILE")
    print("  python cryptocore_simple.py --algorithm aes --mode MODE --decrypt --key KEY --input FILE.enc")
    print("\nПример для CBC:")
    print("  python cryptocore_simple.py --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input файл.txt")
    print('='*60)
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")