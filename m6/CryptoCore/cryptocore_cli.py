#!/usr/bin/env python3
"""
Единый CLI скрипт CryptoCore с поддержкой всех функций
"""

import sys
import os

# Установите правильные пути
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

def main():
    """Главная функция CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="CryptoCore - Cryptographic toolkit",
        prog="cryptocore"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Парсер для dgst команды
    dgst_parser = subparsers.add_parser("dgst", help="Compute hash or HMAC")
    dgst_parser.add_argument("--algorithm", required=True,
                           choices=["sha256", "sha3-256"],
                           help="Hash algorithm")
    dgst_parser.add_argument("--input", required=True,
                           help="Input file")
    dgst_parser.add_argument("--output",
                           help="Output file (optional)")
    dgst_parser.add_argument("--hmac", action="store_true",
                           help="Enable HMAC mode")
    dgst_parser.add_argument("--key",
                           help="Key for HMAC (hex string, required with --hmac)")
    dgst_parser.add_argument("--verify",
                           help="Verify HMAC against file")
    
    args = parser.parse_args()
    
    if args.command != "dgst":
        print("Error: Only 'dgst' command is supported in this version")
        sys.exit(1)
    
    # Импортируем необходимые модули
    try:
        if args.hmac:
            from cryptocore.crypto.mac import HMAC
        else:
            from cryptocore.crypto.hash import SHA256, SHA3_256
    except ImportError:
        print("Error: Could not import crypto modules")
        print("Make sure you are in the correct directory")
        sys.exit(1)
    
    # Проверка файла
    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found")
        sys.exit(1)
    
    # Обработка HMAC
    if args.hmac:
        if not args.key:
            print("Error: --key is required when using --hmac")
            sys.exit(1)
        
        try:
            import binascii
            # Проверяем, что ключ - валидная hex строка
            binascii.unhexlify(args.key)
        except:
            print("Error: Key must be a valid hexadecimal string")
            sys.exit(1)
        
        # Создаем HMAC
        hmac = HMAC(args.key, args.algorithm)
        
        if args.verify:
            # Режим проверки
            if not os.path.exists(args.verify):
                print(f"Error: Verification file '{args.verify}' not found")
                sys.exit(1)
            
            with open(args.verify, 'r') as f:
                verify_content = f.read().strip()
            
            parts = verify_content.split()
            if not parts:
                print("Error: Verification file is empty")
                sys.exit(1)
            
            expected_hmac = parts[0]
            computed_hmac = hmac.compute_file_hex(args.input)
            
            if computed_hmac == expected_hmac:
                print("[OK] HMAC verification successful")
                sys.exit(0)
            else:
                print("[ERROR] HMAC verification failed")
                print(f"  Computed: {computed_hmac}")
                print(f"  Expected: {expected_hmac}")
                sys.exit(1)
        else:
            # Режим генерации
            computed_hmac = hmac.compute_file_hex(args.input)
            output_line = f"{computed_hmac} {args.input}"
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output_line + '\n')
                print(f"HMAC written to: {args.output}")
            else:
                print(output_line)
            
            sys.exit(0)
    
    else:
        # Режим обычного хэширования
        if args.algorithm.lower() in ["sha256", "sha-256"]:
            hasher = SHA256()
        elif args.algorithm.lower() in ["sha3-256", "sha3_256"]:
            hasher = SHA3_256()
        else:
            print(f"Error: Unsupported algorithm '{args.algorithm}'")
            sys.exit(1)
        
        hash_value = hasher.hash_file(args.input)
        output_line = f"{hash_value} {args.input}"
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_line + '\n')
            print(f"Hash written to: {args.output}")
        else:
            print(output_line)
        
        sys.exit(0)

if __name__ == "__main__":
    main()