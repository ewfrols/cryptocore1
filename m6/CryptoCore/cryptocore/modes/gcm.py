"""
Galois/Counter Mode (GCM) implementation.

GCM is an authenticated encryption mode that provides both confidentiality
and authentication. It combines CTR mode for encryption with Galois field
multiplication for authentication.

References:
- NIST SP 800-38D: Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM)
"""

import os
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class AuthenticationError(Exception):
    """Exception raised when GCM authentication fails."""
    pass

class GCM:
    """Galois/Counter Mode (GCM) implementation."""
    
    # Constants for GF(2^128) field
    R = 0xE1000000000000000000000000000000  # Reduction polynomial
    
    def __init__(self, key, nonce=None):
        """
        Initialize GCM with AES key.
        
        Args:
            key: bytes - AES key (16 bytes for AES-128)
            nonce: bytes - nonce (12 bytes recommended)
        """
        if len(key) != 16:
            raise ValueError("GCM requires 16-byte AES-128 key")
        
        self.key = key
        self.nonce = nonce
        
        # Precompute H = E_K(0^128) for GHASH
        self.H = self._aes_encrypt(bytes(16))
        
        # Precompute multiplication table for performance
        self._precompute_mul_table()
    
    def _aes_encrypt(self, data):
        """Encrypt a single 16-byte block using AES."""
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()
    
    def _xor_bytes(self, a, b):
        """XOR two byte strings."""
        return bytes(x ^ y for x, y in zip(a, b))
    
    def _precompute_mul_table(self):
        """Precompute multiplication table for GHASH."""
        self.mul_table = [0] * 16
        self.mul_table[0] = 0
        
        # Compute table[i] = H * i in GF(2^128)
        V_int = self._bytes_to_int(self.H)
        for i in range(1, 16):
            # Multiply by x (right shift and conditionally XOR with R)
            if V_int & 1:
                V_int = (V_int >> 1) ^ self.R
            else:
                V_int >>= 1
            self.mul_table[i] = V_int
    
    def _bytes_to_int(self, b):
        """Convert bytes to integer (big-endian)."""
        return int.from_bytes(b, byteorder='big')
    
    def _int_to_bytes(self, n, length):
        """Convert integer to bytes (big-endian)."""
        return n.to_bytes(length, byteorder='big')
    
    def _right_shift_int(self, n):
        """Right shift a 128-bit integer by 1 bit."""
        return n >> 1
    
    def _gf_mul(self, X, Y):
        """
        Multiply two 128-bit elements in GF(2^128).
        
        Using precomputed table for performance.
        """
        Z = 0
        V = self._bytes_to_int(Y)
        
        # Process X byte by byte
        for i in range(16):
            # Get current byte of X
            byte_val = X[i]
            
            # Process nibbles (4 bits at a time)
            hi_nibble = byte_val >> 4
            lo_nibble = byte_val & 0x0F
            
            # Multiply by H^hi_nibble
            Z ^= self.mul_table[hi_nibble]
            
            # Multiply by x^4 (shift left by 4 bits)
            for _ in range(4):
                if Z & 1:
                    Z = (Z >> 1) ^ self.R
                else:
                    Z >>= 1
            
            # Multiply by H^lo_nibble
            Z ^= self.mul_table[lo_nibble]
            
            # Multiply by x^4 (shift left by 4 bits)
            for _ in range(4):
                if Z & 1:
                    Z = (Z >> 1) ^ self.R
                else:
                    Z >>= 1
        
        return self._int_to_bytes(Z, 16)
    
    def _ghash(self, A, C):
        """
        Compute GHASH for authentication.
        
        Args:
            A: Additional authenticated data (AAD)
            C: Ciphertext
        
        Returns:
            Authentication tag (16 bytes)
        """
        # Prepare blocks: len(A) || len(C) || A || C || padding
        len_A = len(A)
        len_C = len(C)
        
        # Encode lengths as 64-bit big-endian integers
        len_block = struct.pack('>QQ', len_A * 8, len_C * 8)  # bits, not bytes!
        
        # Prepare blocks for processing
        blocks = []
        
        # Add A blocks
        for i in range(0, len_A, 16):
            block = A[i:i+16]
            if len(block) < 16:
                block += b'\x00' * (16 - len(block))
            blocks.append(block)
        
        # Add C blocks
        for i in range(0, len_C, 16):
            block = C[i:i+16]
            if len(block) < 16:
                block += b'\x00' * (16 - len(block))
            blocks.append(block)
        
        # Add length block
        blocks.append(len_block)
        
        # GHASH computation
        Y = bytes(16)
        for block in blocks:
            # XOR then multiply
            Y = self._xor_bytes(Y, block)
            Y = self._gf_mul(Y, self.H)
        
        return Y
    
    def _generate_iv(self, nonce):
        """
        Generate initial counter from nonce.
        
        For 12-byte nonce: IV = nonce || 0x00000001
        For other sizes: IV = GHASH(nonce || padding) XOR len(nonce)
        """
        if len(nonce) == 12:
            # Standard 12-byte nonce
            return nonce + b'\x00\x00\x00\x01'
        else:
            # Non-standard size
            # Pad nonce to multiple of 16
            padded_nonce = nonce
            if len(padded_nonce) % 16 != 0:
                padded_nonce += b'\x00' * (16 - len(padded_nonce) % 16)
            
            # Add length block
            len_block = struct.pack('>Q', len(nonce) * 8)
            padded_nonce += len_block
            
            # GHASH the padded nonce
            return self._ghash(b'', padded_nonce)
    
    def encrypt(self, nonce, plaintext, aad=b''):
        """
        Encrypt data using GCM.
        
        Args:
            nonce: bytes - unique nonce (12 bytes recommended)
            plaintext: bytes - data to encrypt
            aad: bytes - additional authenticated data
        
        Returns:
            tuple: (ciphertext, tag)
        """
        if self.nonce is not None:
            nonce = self.nonce
        
        # Generate J0 (initial counter)
        J0 = self._generate_iv(nonce)
        
        # First counter for authentication tag (incremented after encryption)
        J0_int = self._bytes_to_int(J0)
        inc_counter = (J0_int + 1) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        auth_counter = self._int_to_bytes(inc_counter, 16)
        
        # Generate keystream using CTR mode
        ciphertext = bytearray()
        num_blocks = (len(plaintext) + 15) // 16
        
        for i in range(num_blocks):
            # Increment counter for each block
            counter = (J0_int + 1 + i) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            counter_bytes = self._int_to_bytes(counter, 16)
            
            # Encrypt counter to get keystream
            keystream = self._aes_encrypt(counter_bytes)
            
            # XOR with plaintext block
            block_start = i * 16
            block_end = min((i + 1) * 16, len(plaintext))
            block = plaintext[block_start:block_end]
            
            # If last block is partial, use only needed bytes
            keystream_len = block_end - block_start
            ciphertext_block = self._xor_bytes(block, keystream[:keystream_len])
            ciphertext.extend(ciphertext_block)
        
        ciphertext = bytes(ciphertext)
        
        # Compute authentication tag
        S = self._aes_encrypt(auth_counter)
        auth_tag_input = self._ghash(aad, ciphertext)
        tag = self._xor_bytes(auth_tag_input, S)
        
        return ciphertext, tag[:16]  # Tag is truncated to desired length
    
    def decrypt(self, nonce, ciphertext, tag, aad=b''):
        """
        Decrypt and verify data using GCM.
        
        Args:
            nonce: bytes - nonce used for encryption
            ciphertext: bytes - encrypted data
            tag: bytes - authentication tag (16 bytes)
            aad: bytes - additional authenticated data
        
        Returns:
            bytes: decrypted plaintext
        
        Raises:
            AuthenticationError: if tag verification fails
        """
        if self.nonce is not None:
            nonce = self.nonce
        
        # First verify authentication tag
        J0 = self._generate_iv(nonce)
        J0_int = self._bytes_to_int(J0)
        inc_counter = (J0_int + 1) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        auth_counter = self._int_to_bytes(inc_counter, 16)
        
        # Compute expected tag
        S = self._aes_encrypt(auth_counter)
        auth_tag_input = self._ghash(aad, ciphertext)
        expected_tag = self._xor_bytes(auth_tag_input, S)
        
        # Compare tags (constant time)
        if not self._constant_time_compare(tag[:16], expected_tag[:16]):
            raise AuthenticationError("GCM authentication failed")
        
        # Decrypt using CTR mode
        plaintext = bytearray()
        num_blocks = (len(ciphertext) + 15) // 16
        
        for i in range(num_blocks):
            # Increment counter for each block
            counter = (J0_int + 1 + i) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            counter_bytes = self._int_to_bytes(counter, 16)
            
            # Encrypt counter to get keystream
            keystream = self._aes_encrypt(counter_bytes)
            
            # XOR with ciphertext block
            block_start = i * 16
            block_end = min((i + 1) * 16, len(ciphertext))
            block = ciphertext[block_start:block_end]
            
            # If last block is partial, use only needed bytes
            keystream_len = block_end - block_start
            plaintext_block = self._xor_bytes(block, keystream[:keystream_len])
            plaintext.extend(plaintext_block)
        
        return bytes(plaintext)
    
    def _constant_time_compare(self, a, b):
        """Constant time comparison to prevent timing attacks."""
        if len(a) != len(b):
            return False
        
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0