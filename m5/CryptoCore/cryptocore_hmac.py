#!/usr/bin/env python3
"""
Упрощенный CLI для HMAC (если основной не работает)
"""

import sys
import os
import argparse
import binascii

# Добавить путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from cryptocore.crypto.mac import HMAC
    print("✓ HMAC импортирован успешно", file=sys.stderr)
except ImportError as e:
    print(f"✗ Ошибка импорта: {e}", file=sys.stderr)
    print("Попытка прямого импорта...", file=sys.stderr)
    
    # Прямой импорт
    import sys
    sys.path.insert(0, 'cryptocore')
    from crypto.mac import HMAC
    print("✓ HMAC импортирован через прямой путь", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="CryptoCore HMAC Tool - Generate and verify HMAC-SHA256",
        prog="cryptocore-hmac"
    )
    
    parser.add_argument("--algorithm", default="sha256", choices=["sha256"],
                       help="Hash algorithm (only sha256 supported)")
    parser.add_argument("--hmac", action="store_true", default=True,
                       help="Enable HMAC mode (always on)")
    parser.add_argument("--key", required=True,
                       help="Key for HMAC (hex string)")
    parser.add_argument("--input", required=True,
                       help="Input file")
    parser.add_argument("--output",
                       help="Output file for HMAC (optional)")
    parser.add_argument("--verify",
                       help="Verify HMAC against file")
    
    args = parser.parse_args()
    
    # Проверка файла
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Проверка ключа
    try:
        # Проверим, что ключ - валидная hex строка
        key_bytes = binascii.unhexlify(args.key)
    except (ValueError, binascii.Error):
        print(f"Error: Key must be a valid hexadecimal string", file=sys.stderr)
        sys.exit(1)
    
    # Создаем HMAC
    try:
        hmac = HMAC(args.key, args.algorithm)
    except Exception as e:
        print(f"Error creating HMAC: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.verify:
        # Режим проверки
        if not os.path.exists(args.verify):
            print(f"Error: Verification file '{args.verify}' not found", file=sys.stderr)
            sys.exit(1)
        
        # Читаем ожидаемый HMAC
        with open(args.verify, 'r') as f:
            verify_content = f.read().strip()
        
        # Парсим (формат: HMAC_VALUE [FILENAME])
        parts = verify_content.split()
        if not parts:
            print("Error: Verification file is empty", file=sys.stderr)
            sys.exit(1)
        
        expected_hmac = parts[0]
        
        # Вычисляем HMAC
        computed_hmac = hmac.compute_file_hex(args.input)
        
        # Сравниваем
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
            try:
                with open(args.output, 'w') as f:
                    f.write(output_line + '\n')
                print(f"HMAC written to: {args.output}")
            except IOError as e:
                print(f"Error writing to file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(output_line)
        
        sys.exit(0)

if __name__ == "__main__":
    main()