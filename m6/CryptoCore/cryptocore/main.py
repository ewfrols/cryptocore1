#!/usr/bin/env python3

import sys
import os
import binascii
import tempfile
import shutil

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
    """Handle encryption/decryption with AEAD support (Sprint 6)."""
    try:
        # Validate file exists
        if not os.path.exists(args.input):
            print(f"Error: File '{args.input}' not found", file=sys.stderr)
            return False
        
        # Parse key
        key = bytes.fromhex(args.key)
        
        # Parse AAD if provided
        aad = b""
        if args.aad:
            aad = bytes.fromhex(args.aad)
        
        # Parse IV/nonce if provided
        iv = None
        if args.iv:
            iv = bytes.fromhex(args.iv)
        
        # Get mode class from modes module
        try:
            from cryptocore.modes import MODES
            mode_class = MODES.get(args.mode.lower())
            if not mode_class:
                print(f"Error: Unknown mode '{args.mode}'", file=sys.stderr)
                return False
        except ImportError:
            print("Error: Could not import modes module", file=sys.stderr)
            return False
        
        if args.mode.lower() == "gcm":
            # GCM mode (Sprint 6)
            return handle_gcm_mode(args, key, iv, aad, mode_class)
        else:
            # Legacy modes (Sprints 1-3)
            return handle_legacy_mode(args, key, iv, aad, mode_class)
            
    except ValueError as e:
        print(f"Error: Invalid hex string - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def handle_gcm_mode(args, key, iv, aad, gcm_class):
    """Handle GCM encryption/decryption."""
    try:
        if args.encrypt:
            # GCM Encryption
            return gcm_encrypt(args, key, iv, aad, gcm_class)
        else:
            # GCM Decryption
            return gcm_decrypt(args, key, iv, aad, gcm_class)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False

def gcm_encrypt(args, key, iv, aad, gcm_class):
    """GCM encryption."""
    try:
        # Read plaintext
        with open(args.input, 'rb') as f:
            plaintext = f.read()
        
        # Create GCM instance
        if iv:
            gcm = gcm_class(key, iv)
        else:
            # Generate random nonce (12 bytes)
            gcm = gcm_class(key)
        
        # Encrypt
        ciphertext_with_nonce_and_tag = gcm.encrypt(plaintext, aad)
        
        # Write output
        if args.output:
            # Create temp file first (for safety)
            temp_filename = None
            try:
                with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                    temp_file.write(ciphertext_with_nonce_and_tag)
                    temp_filename = temp_file.name
                
                # Move temp file to final location
                shutil.move(temp_filename, args.output)
                print(f"[SUCCESS] Encryption completed successfully")
                print(f"Nonce: {gcm.nonce.hex()}")
                print(f"Output format: 12-byte nonce + ciphertext + 16-byte tag")
                return True
            finally:
                if temp_filename and os.path.exists(temp_filename):
                    os.unlink(temp_filename)
        else:
            # Write to stdout
            sys.stdout.buffer.write(ciphertext_with_nonce_and_tag)
            return True
            
    except Exception as e:
        print(f"Error during GCM encryption: {e}", file=sys.stderr)
        return False

def gcm_decrypt(args, key, iv, aad, gcm_class):
    """GCM decryption with authentication."""
    try:
        # Read ciphertext (contains nonce || ciphertext || tag)
        with open(args.input, 'rb') as f:
            data = f.read()
        
        if len(data) < 28:  # Minimum size (12 nonce + 0 ciphertext + 16 tag)
            print("Error: Input file too small for GCM format", file=sys.stderr)
            return False
        
        if iv:
            # Use provided nonce
            nonce = iv
            # Data should contain only ciphertext + tag in this case
            ciphertext_with_tag = data
        else:
            # Extract nonce from data (first 12 bytes)
            if len(data) < 12:
                print("Error: Input file too small to contain nonce", file=sys.stderr)
                return False
            nonce = data[:12]
            ciphertext_with_tag = data
            iv = nonce  # Set iv for GCM constructor
        
        # Create GCM instance with nonce
        gcm = gcm_class(key, iv)
        
        # Decrypt with authentication
        try:
            plaintext = gcm.decrypt(ciphertext_with_tag, aad)
        except Exception as e:
            print(f"[ERROR] Authentication failed: {e}", file=sys.stderr)
            print("No output file created due to authentication failure.", file=sys.stderr)
            return False
        
        # Write output (only if authentication succeeded)
        if args.output:
            # Create temp file first
            temp_filename = None
            try:
                with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                    temp_file.write(plaintext)
                    temp_filename = temp_file.name
                
                # Move temp file to final location
                shutil.move(temp_filename, args.output)
                print("[SUCCESS] Decryption completed successfully")
                return True
            finally:
                if temp_filename and os.path.exists(temp_filename):
                    os.unlink(temp_filename)
        else:
            # Write to stdout
            sys.stdout.buffer.write(plaintext)
            return True
            
    except Exception as e:
        print(f"Error during GCM decryption: {e}", file=sys.stderr)
        return False

def handle_legacy_mode(args, key, iv, aad, mode_class):
    """Handle legacy encryption modes (Sprints 1-3)."""
    try:
        # Read input file
        with open(args.input, 'rb') as f:
            data = f.read()
        
        # For this simplified version, just show info
        print(f"Legacy mode {args.mode.upper()} functionality")
        print(f"Command: {'ENCRYPT' if args.encrypt else 'DECRYPT'}")
        print(f"Input file: {args.input} ({len(data)} bytes)")
        print(f"Key: {args.key[:16]}...")
        
        if iv:
            print(f"IV/Nonce: {iv.hex()[:16]}...")
        
        if aad:
            print(f"AAD: {aad.hex()[:16]}... (not used in legacy modes)")
        
        if args.output:
            print(f"Would write output to: {args.output}")
            # For demo, just copy input to output
            with open(args.output, 'wb') as f:
                f.write(data)
            print(f"[INFO] Demo: Copied input to output (no actual encryption)")
        else:
            print("No output file specified")
        
        return True
        
    except Exception as e:
        print(f"Error in legacy mode: {e}", file=sys.stderr)
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