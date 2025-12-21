#!/usr/bin/env python3

import sys
import os
import binascii

def handle_dgst_command(args):
    """Handle digest (hash) and HMAC commands."""
    try:
        if args.hmac:
            # HMAC mode (Sprint 5)
            return handle_hmac_command(args)
        else:
            # Regular hash mode (Sprint 4)
            return handle_hash_command(args)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def handle_hash_command(args):
    """Handle regular hash command (Sprint 4)."""
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

def handle_hmac_command(args):
    """Handle HMAC command (Sprint 5)."""
    from cryptocore.crypto.mac import HMAC
    
    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        return False
    
    # Create HMAC instance
    try:
        hmac = HMAC(args.key, args.algorithm)
    except Exception as e:
        print(f"Error creating HMAC: {e}", file=sys.stderr)
        return False
    
    if args.verify:
        # Verification mode
        return verify_hmac(hmac, args.input, args.verify)
    else:
        # Generation mode
        return generate_hmac(hmac, args.input, args.output)

def generate_hmac(hmac, input_file, output_file=None):
    """Generate HMAC for a file."""
    try:
        # Compute HMAC
        hmac_value = hmac.compute_file_hex(input_file)
        
        # Format output: HMAC_VALUE INPUT_FILE_PATH
        output_line = f"{hmac_value} {input_file}"
        
        # Output to file or stdout
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(output_line + '\n')
                print(f"HMAC written to: {output_file}")
            except IOError as e:
                print(f"Error writing to file: {e}", file=sys.stderr)
                return False
        else:
            print(output_line)
        
        return True
        
    except Exception as e:
        print(f"Error computing HMAC: {e}", file=sys.stderr)
        return False

def verify_hmac(hmac, input_file, verify_file):
    """Verify HMAC against expected value in file."""
    try:
        if not os.path.exists(verify_file):
            print(f"Error: Verification file '{verify_file}' not found", file=sys.stderr)
            return False
        
        # Read expected HMAC from file
        with open(verify_file, 'r') as f:
            verify_content = f.read().strip()
        
        # Parse expected HMAC (format: HMAC_VALUE [FILENAME])
        parts = verify_content.split()
        if not parts:
            print(f"Error: Verification file is empty", file=sys.stderr)
            return False
        
        expected_hmac_hex = parts[0]
        
        # Compute HMAC for input file
        computed_hmac_hex = hmac.compute_file_hex(input_file)
        
        # Compare
        if computed_hmac_hex == expected_hmac_hex:
            print("[OK] HMAC verification successful")
            return True
        else:
            print("[ERROR] HMAC verification failed")
            print(f"  Computed: {computed_hmac_hex}")
            print(f"  Expected: {expected_hmac_hex}")
            return False
            
    except Exception as e:
        print(f"Error during verification: {e}", file=sys.stderr)
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
        sys.exit(1)
    
    if args.command == "dgst":
        success = handle_dgst_command(args)
        sys.exit(0 if success else 1)
    elif args.command == "encrypt":
        success = handle_encrypt_decrypt_command(args)
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()