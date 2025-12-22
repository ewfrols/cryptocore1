#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CryptoCore SIMPLE - исправленная версия с поддержкой GCM (Windows compatible)
"""

import os
import sys
import argparse

# Добавляем текущую папку в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def gcm_command(args):
    """Обработка команд GCM"""
    try:
        from cryptocore.modes.gcm import GCM
        
        # Читаем ключ
        if len(args.key) == 32:  # 16 байт в hex
            key = bytes.fromhex(args.key)
        else:
            raise ValueError(f"Ключ должен быть 32 hex-символа (16 байт), получено {len(args.key)}")
        
        # Читаем AAD если есть (может быть hex или текст)
        aad = b""
        if args.aad:
            try:
                # Пробуем интерпретировать как hex
                aad = bytes.fromhex(args.aad)
            except ValueError:
                # Если не hex, используем как текст
                aad = args.aad.encode('utf-8')
        
        # Читаем входной файл
        with open(args.input, 'rb') as f:
            data = f.read()
        
        # Для шифрования
        if args.encrypt:
            print(f"[GCM] Шифрование...")
            print(f"   Ключ: {args.key}")
            print(f"   AAD: {args.aad if args.aad else '(нет)'}")
            print(f"   Файл: {args.input} ({len(data)} байт)")
            
            # Создаем GCM объект
            gcm = GCM(key)
            
            # Генерируем случайный nonce (12 байт)
            import secrets
            nonce = secrets.token_bytes(12)
            
            ciphertext, tag = gcm.encrypt(nonce, data, aad)
            
            # Сохраняем результат: nonce (12) + tag (16) + ciphertext
            result = nonce + tag + ciphertext
            
            # Записываем в файл
            output_file = args.output if args.output else args.input + '.enc'
            with open(output_file, 'wb') as f:
                f.write(result)
            
            print(f"[OK] Успешно зашифровано!")
            print(f"   Nonce: {nonce.hex()}")
            print(f"   Tag: {tag.hex()}")
            print(f"   Результат сохранен в: {output_file}")
            print(f"   Общий размер: {len(result)} байт")
        
        # Для дешифрования
        elif args.decrypt:
            print(f"[GCM] Дешифрование...")
            print(f"   Ключ: {args.key}")
            print(f"   AAD: {args.aad if args.aad else '(нет)'}")
            print(f"   Файл: {args.input}")
            
            # Читаем зашифрованные данные
            with open(args.input, 'rb') as f:
                encrypted_data = f.read()
            
            # Разбираем данные: первые 12 байт - nonce, следующие 16 байт - tag, остальное - ciphertext
            if len(encrypted_data) < 28:  # 12 + 16 = 28 минимальный размер
                raise ValueError(f"Файл слишком мал для GCM данных: {len(encrypted_data)} байт")
            
            nonce = encrypted_data[:12]
            tag = encrypted_data[12:28]
            ciphertext = encrypted_data[28:]
            
            print(f"   Прочитано: {len(encrypted_data)} байт")
            print(f"   Nonce: {nonce.hex()}")
            print(f"   Tag: {tag.hex()}")
            print(f"   Ciphertext: {len(ciphertext)} байт")
            
            # Создаем GCM объект и дешифруем
            gcm = GCM(key)
            
            try:
                plaintext = gcm.decrypt(nonce, ciphertext, tag, aad)
                
                # Сохраняем результат
                output_file = args.output if args.output else args.input + '.dec'
                with open(output_file, 'wb') as f:
                    f.write(plaintext)
                
                print(f"[OK] Успешно дешифровано!")
                print(f"   Результат сохранен в: {output_file}")
                print(f"   Размер расшифрованного: {len(plaintext)} байт")
                
            except Exception as e:
                print(f"[ERROR] Ошибка аутентификации: {e}")
                print("Файл был изменен или использован неверный ключ/AAD!")
                sys.exit(1)
    
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def dgst_command(args):
    """Обработка команд хэширования/HMAC"""
    try:
        # Читаем файл
        with open(args.input, 'rb') as f:
            data = f.read()
        
        # HMAC
        if args.hmac:
            print(f"[HMAC] Вычисление...")
            print(f"   Алгоритм: {args.algorithm}")
            print(f"   Ключ: {args.key}")
            print(f"   Файл: {args.input} ({len(data)} байт)")
            
            from cryptocore.crypto.mac.hmac import HMAC
            
            # Создаем HMAC
            hmac = HMAC(args.key, hash_algorithm=args.algorithm)
            hmac.update(data)
            hmac_result = hmac.hexdigest()
            
            print(f"[OK] HMAC: {hmac_result}")
            
            # Если нужно проверить
            if args.verify:
                print(f"[HMAC] Проверка...")
                with open(args.verify, 'r') as f:
                    expected_hmac = f.read().strip()
                
                if hmac_result == expected_hmac:
                    print(f"[OK] HMAC проверка пройдена!")
                else:
                    print(f"[ERROR] HMAC не совпадает!")
                    print(f"   Ожидалось: {expected_hmac}")
                    print(f"   Получено:  {hmac_result}")
                    sys.exit(1)
            
            # Записываем результат если указан output
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(hmac_result)
        
        # Обычное хэширование
        else:
            print(f"[HASH] Хэширование...")
            print(f"   Алгоритм: {args.algorithm}")
            print(f"   Файл: {args.input} ({len(data)} байт)")
            
            if args.algorithm == 'sha256':
                from cryptocore.crypto.hash.sha256_final import SHA256
                sha = SHA256()
                sha.update(data)
                hash_result = sha.hexdigest()
            elif args.algorithm == 'sha3-256':
                import hashlib
                hash_result = hashlib.sha3_256(data).hexdigest()
            else:
                raise ValueError(f"Неподдерживаемый алгоритм: {args.algorithm}")
            
            print(f"[OK] Хэш: {hash_result}")
            
            # Записываем результат если указан output
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(hash_result)
    
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description='CryptoCore SIMPLE - полная поддержка всех режимов (Windows)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # GCM шифрование (AAD может быть hex или текст)
  python cryptocore_simple.py gcm --encrypt --key 00112233445566778899aabbccddeeff --aad aabbcc --input file.txt
  python cryptocore_simple.py gcm --encrypt --key 00112233445566778899aabbccddeeff --aad "my aad" --input file.txt
  
  # GCM дешифрование
  python cryptocore_simple.py gcm --decrypt --key 00112233445566778899aabbccddeeff --aad aabbcc --input file.enc
  
  # HMAC
  python cryptocore_simple.py dgst --algorithm sha256 --hmac --key mykey --input file.txt
  python cryptocore_simple.py dgst --algorithm sha256 --hmac --key 00112233 --input file.txt
  
  # Обычное хэширование
  python cryptocore_simple.py dgst --algorithm sha256 --input file.txt
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Команды')
    
    # GCM парсер
    gcm_parser = subparsers.add_parser('gcm', help='GCM шифрование/дешифрование')
    gcm_parser.add_argument('--encrypt', action='store_true', help='Шифрование')
    gcm_parser.add_argument('--decrypt', action='store_true', help='Дешифрование')
    gcm_parser.add_argument('--key', required=True, help='Ключ (32 hex-символа)')
    gcm_parser.add_argument('--aad', help='Дополнительные аутентифицированные данные (hex или текст)')
    gcm_parser.add_argument('--input', required=True, help='Входной файл')
    gcm_parser.add_argument('--output', help='Выходной файл')
    
    # DGST парсер
    dgst_parser = subparsers.add_parser('dgst', help='Хэширование/HMAC')
    dgst_parser.add_argument('--algorithm', choices=['sha256', 'sha3-256'], default='sha256', help='Алгоритм хэширования')
    dgst_parser.add_argument('--hmac', action='store_true', help='Использовать HMAC')
    dgst_parser.add_argument('--key', help='Ключ для HMAC (hex или строка)')
    dgst_parser.add_argument('--input', required=True, help='Входной файл')
    dgst_parser.add_argument('--output', help='Выходной файл')
    dgst_parser.add_argument('--verify', help='Файл с HMAC для проверки')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("CRYPTOCORE SIMPLE - полная поддержка GCM и HMAC")
    print("=" * 60)
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'gcm':
        gcm_command(args)
    elif args.command == 'dgst':
        dgst_command(args)

if __name__ == "__main__":
    main()