"""
Authenticated Encryption with Associated Data (AEAD) implementations.
Sprint 6: GCM and Encrypt-then-MAC.
"""

from .encrypt_then_mac import EncryptThenMAC

__all__ = ['EncryptThenMAC']

__version__ = "1.0.0"
__author__ = "CryptoCore Team"