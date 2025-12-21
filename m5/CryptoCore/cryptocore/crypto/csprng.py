"""
Cryptographically Secure Pseudorandom Number Generator (CSPRNG)
Implementation for Sprint 3 requirements.
"""

import os
import sys


def generate_random_bytes(num_bytes: int) -> bytes:
    """
    Generate cryptographically secure random bytes using os.urandom().
    
    Args:
        num_bytes: Number of bytes to generate (must be positive).
    
    Returns:
        Bytes object containing random data.
    
    Raises:
        ValueError: If num_bytes <= 0
        RuntimeError: If os.urandom fails
    """
    if num_bytes <= 0:
        raise ValueError(f"Number of bytes must be positive, got {num_bytes}")
    
    try:
        return os.urandom(num_bytes)
    except Exception as e:
        raise RuntimeError(f"CSPRNG failure: {e}")


# Quick test if run directly
if __name__ == "__main__":
    print("Testing CSPRNG module...")
    test_data = generate_random_bytes(32)
    print(f"Generated 32 bytes: {test_data.hex()[:64]}...")
    print("✓ CSPRNG module is functional")