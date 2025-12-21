#!/usr/bin/env python3

import sys
import os
import argparse

def handle_dgst_command(args):
    """Handle digest (hash) command."""
    try:
        # Локальный импорт для избежания циклических зависимостей
        from cryptocore.crypto.hash import SHA256, SHA3_256
        
        if not os.path.exists(args.input):
            print(f"Error: File '{args.input}' not found", file=sys.stderr)
            return False
        
        # Select algorithm
        algorithm_lower = args.algorithm.lower()
        if algorithm_lower in ['sha256', 'sha-256']:
            hasher = SHA256()
        elif algorithm_lower in ['sha3-256', 'sha3_256']:
            hasher = SHA3_256()
        else:
            print(f"Error: Unsupported algorithm '{args.algorithm}'", file=sys.stderr)
            return False
        
        # Compute hash
        hash_value = hasher.hash_file(args.input)
        
        # Format output: HASH_VALUE INPUT_FILE_PATH
        output_line = f"{hash_value} {args.input}"
        
        # Output to file or stdout
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    f.write(output_line + '\n')
                print(f"Hash written to: {args.output}")
            except IOError as e:
                print(f"Error writing to file: {e}", file=sys.stderr)
                return False
        else:
            print(output_line)
        
        return True
        
    except Exception as e:
        print(f"Error computing hash: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def handle_encrypt_decrypt_command(args):
    """Handle encryption/decryption command (existing functionality)."""
    try:
        # Ваш существующий код для шифрования/дешифрования
        # ... (оставьте без изменений)
        
        # Временная заглушка
        print("Encryption/decryption functionality (from previous sprints)")
        print(f"Command: {'encrypt' if args.encrypt else 'decrypt'}")
        print(f"Input: {args.input}")
        print(f"Mode: {args.mode}")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False

def main():
    """Main entry point."""
    try:
        from cryptocore.cli_parser import parse_arguments
        args = parse_arguments()
    except ImportError as e:
        print(f"Error importing CLI parser: {e}", file=sys.stderr)
        # Fallback to simple parser
        args = simple_parse_arguments()
    
    if args.command == "dgst":
        success = handle_dgst_command(args)
        sys.exit(0 if success else 1)
    elif args.command == "encrypt":
        success = handle_encrypt_decrypt_command(args)
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)

def simple_parse_arguments():
    """Simple argument parser as fallback."""
    parser = argparse.ArgumentParser(description="CryptoCore - Simple fallback")
    parser.add_argument("command", choices=["dgst", "encrypt"])
    
    # Digest arguments
    parser.add_argument("--algorithm", help="Hash algorithm")
    parser.add_argument("--input", help="Input file")
    parser.add_argument("--output", help="Output file")
    
    # Parse only known args
    args, unknown = parser.parse_known_args()
    
    # For dgst command, parse additional args
    if args.command == "dgst":
        dgst_parser = argparse.ArgumentParser()
        dgst_parser.add_argument("--algorithm", required=True)
        dgst_parser.add_argument("--input", required=True)
        dgst_parser.add_argument("--output")
        
        # Re-parse with dgst parser
        dgst_args = dgst_parser.parse_args(unknown)
        
        # Merge args
        for attr in ['algorithm', 'input', 'output']:
            if hasattr(dgst_args, attr):
                setattr(args, attr, getattr(dgst_args, attr))
    
    return args

if __name__ == "__main__":
    main()