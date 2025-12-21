#!/usr/bin/env python3
"""
Рабочий скрипт для команды dgst (временное решение)
"""

import sys
import os
import argparse

# Добавить путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cryptocore.crypto.hash import SHA256, SHA3_256

def main():
    parser = argparse.ArgumentParser(
        description="CryptoCore dgst - Compute message digests",
        prog="cryptocore dgst"
    )
    
    parser.add_argument("--algorithm", required=True,
                       choices=["sha256", "sha3-256", "sha3_256"],
                       help="Hash algorithm to use")
    parser.add_argument("--input", required=True,
                       help="Input file to hash")
    parser.add_argument("--output",
                       help="Output file for hash (optional)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Select algorithm
    algorithm_lower = args.algorithm.lower()
    if algorithm_lower in ['sha256', 'sha-256']:
        hasher = SHA256()
    elif algorithm_lower in ['sha3-256', 'sha3_256']:
        hasher = SHA3_256()
    else:
        print(f"Error: Unsupported algorithm '{args.algorithm}'", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Compute hash
        hash_value = hasher.hash_file(args.input)
        
        # Format output: HASH_VALUE INPUT_FILE_PATH
        output_line = f"{hash_value} {args.input}"
        
        # Output to file or stdout
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_line + '\n')
            print(f"Hash written to: {args.output}")
        else:
            print(output_line)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()