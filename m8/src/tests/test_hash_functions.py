#!/usr/bin/env python3
"""
Comprehensive test suite for hash functions
Tests Sprint 4 hash implementations
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cryptocore.hash.sha256 import SHA256, sha256_hash, sha256_file
from cryptocore.hash.sha3_256 import SHA3_256, sha3_256_hash, sha3_256_file

def test_sha256_known_answers():
    print("Testing SHA-256 with known answers...")
    
    test_vectors = [
        ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    ]
    
    for test_input, expected in test_vectors:
        result = sha256_hash(test_input.encode('utf-8') if test_input else b"")
        if result == expected:
            print(f"  PASS: '{test_input[:20]}...' -> {expected[:16]}...")
        else:
            print(f"  FAIL: '{test_input}'")
            return False
    
    print("  All SHA-256 known answer tests passed")
    return True

def test_sha3_256_known_answers():
    print("Testing SHA3-256 with known answers...")
    
    test_vectors = [
        ("", "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"),
        ("abc", "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"),
    ]
    
    for test_input, expected in test_vectors:
        result = sha3_256_hash(test_input.encode('utf-8') if test_input else b"")
        if result == expected:
            print(f"  PASS: '{test_input[:20]}...' -> {expected[:16]}...")
        else:
            print(f"  FAIL: '{test_input}'")
            return False
    
    print("  All SHA3-256 known answer tests passed")
    return True

if __name__ == "__main__":
    print("Hash Functions Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    try:
        all_passed &= test_sha256_known_answers()
        print()
        
        all_passed &= test_sha3_256_known_answers()
        print()
        
        if all_passed:
            print("All hash function tests passed!")
        else:
            print("Some tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test suite failed with exception: {e}")
        sys.exit(1)