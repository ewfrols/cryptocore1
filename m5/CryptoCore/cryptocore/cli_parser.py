import argparse
import os
import sys
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CryptoCore - Cryptographic toolkit for encryption, decryption, hashing, and MAC",
        prog="cryptocore"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    
    # Encrypt/Decrypt command (existing)
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt or decrypt files")
    encrypt_parser.add_argument("--key", type=str, help="Encryption key (hex string or file)")
    encrypt_parser.add_argument("--mode", type=str, choices=["ecb", "cbc", "cfb", "ofb", "ctr"], 
                              default="cbc", help="Block cipher mode")
    encrypt_parser.add_argument("--input", type=str, required=True, help="Input file path")
    encrypt_parser.add_argument("--output", type=str, help="Output file path")
    encrypt_parser.add_argument("--encrypt", action="store_true", help="Encrypt mode")
    encrypt_parser.add_argument("--decrypt", action="store_true", help="Decrypt mode")
    encrypt_parser.add_argument("--iv", type=str, help="Initialization vector (hex string)")
    
    # Digest/Hash command (Sprint 4, updated for Sprint 5)
    digest_parser = subparsers.add_parser("dgst", help="Compute message digest (hash) or MAC")
    digest_parser.add_argument("--algorithm", type=str, required=True,
                             choices=["sha256", "sha3-256", "sha3_256"],
                             help="Hash algorithm to use")
    digest_parser.add_argument("--input", type=str, required=True,
                             help="Input file to hash")
    digest_parser.add_argument("--output", type=str,
                             help="Output file for hash (optional)")
    
    # NEW in Sprint 5: HMAC options
    digest_parser.add_argument("--hmac", action="store_true",
                             help="Enable HMAC mode (requires --key)")
    digest_parser.add_argument("--key", type=str,
                             help="Key for HMAC (hex string, required with --hmac)")
    digest_parser.add_argument("--verify", type=str,
                             help="Verify HMAC against file (requires --hmac and --key)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.command == "encrypt":
        if not args.encrypt and not args.decrypt:
            parser.error("Either --encrypt or --decrypt must be specified")
        if args.encrypt and args.decrypt:
            parser.error("Cannot specify both --encrypt and --decrypt")
        if not args.key:
            parser.error("--key is required for encryption/decryption")
    
    elif args.command == "dgst":
        if not os.path.exists(args.input):
            parser.error(f"Input file does not exist: {args.input}")
        
        # HMAC validation
        if args.hmac:
            if not args.key:
                parser.error("--key is required when using --hmac")
            # Validate key format (should be hex string)
            try:
                bytes.fromhex(args.key)
            except ValueError:
                parser.error("--key must be a valid hexadecimal string")
        else:
            if args.key:
                parser.error("--key can only be used with --hmac")
            if args.verify:
                parser.error("--verify can only be used with --hmac")
    
    return args


# Для обратной совместимости со старым кодом
def ПарсерАргументов():
    """Alias for backward compatibility."""
    return parse_arguments()