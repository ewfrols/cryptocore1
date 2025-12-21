import struct
import binascii

class HMAC:
    """HMAC implementation from scratch following RFC 2104."""
    
    def __init__(self, key, hash_algo='sha256'):
        """
        Initialize HMAC with a key and hash algorithm.
        
        Args:
            key: bytes or hex string - the secret key
            hash_algo: string - hash algorithm to use ('sha256' only for now)
        """
        from ..hash import SHA256
        
        if hash_algo.lower() != 'sha256':
            raise ValueError("Only SHA-256 is supported for HMAC in this implementation")
        
        self.hash_function = SHA256
        self.block_size = 64  # Block size for SHA-256 (bytes)
        
        # Convert key to bytes if needed
        if isinstance(key, str):
            # Try to interpret as hex string
            try:
                self.key = bytes.fromhex(key)
            except ValueError:
                # If not hex, treat as plain text
                self.key = key.encode('utf-8')
        else:
            self.key = bytes(key)
        
        # Process key according to RFC 2104
        self.key = self._process_key(self.key)
    
    def _process_key(self, key):
        """Process key according to RFC 2104."""
        # If key is longer than block size, hash it
        if len(key) > self.block_size:
            hasher = self.hash_function()
            hasher.update(key)
            key = hasher.digest()
        
        # If key is shorter than block size, pad with zeros
        if len(key) < self.block_size:
            key = key + b'\x00' * (self.block_size - len(key))
        
        return key
    
    @staticmethod
    def _xor_bytes(a, b):
        """XOR two byte strings of equal length."""
        return bytes(x ^ y for x, y in zip(a, b))
    
    def compute(self, message):
        """
        Compute HMAC for a message.
        
        HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
        where H is SHA-256, opad = 0x5c repeated, ipad = 0x36 repeated.
        
        Args:
            message: bytes - message to authenticate
        
        Returns:
            bytes: HMAC value
        """
        # Create inner and outer pads
        ipad = self._xor_bytes(self.key, b'\x36' * self.block_size)
        opad = self._xor_bytes(self.key, b'\x5c' * self.block_size)
        
        # Inner hash: H((K ⊕ ipad) || message)
        inner_hasher = self.hash_function()
        inner_hasher.update(ipad)
        inner_hasher.update(message)
        inner_hash = inner_hasher.digest()
        
        # Outer hash: H((K ⊕ opad) || inner_hash)
        outer_hasher = self.hash_function()
        outer_hasher.update(opad)
        outer_hasher.update(inner_hash)
        
        return outer_hasher.digest()
    
    def compute_hex(self, message):
        """Compute HMAC and return as hexadecimal string."""
        return binascii.hexlify(self.compute(message)).decode()
    
    def compute_file(self, filepath, chunk_size=8192):
        """
        Compute HMAC for a file in chunks.
        
        Args:
            filepath: string - path to file
            chunk_size: int - size of chunks to read
        
        Returns:
            bytes: HMAC value
        """
        import os
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Create inner and outer pads
        ipad = self._xor_bytes(self.key, b'\x36' * self.block_size)
        opad = self._xor_bytes(self.key, b'\x5c' * self.block_size)
        
        # Inner hash: H((K ⊕ ipad) || message)
        inner_hasher = self.hash_function()
        inner_hasher.update(ipad)
        
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                inner_hasher.update(chunk)
        
        inner_hash = inner_hasher.digest()
        
        # Outer hash: H((K ⊕ opad) || inner_hash)
        outer_hasher = self.hash_function()
        outer_hasher.update(opad)
        outer_hasher.update(inner_hash)
        
        return outer_hasher.digest()
    
    def compute_file_hex(self, filepath, chunk_size=8192):
        """Compute HMAC for a file and return as hex string."""
        return binascii.hexlify(self.compute_file(filepath, chunk_size)).decode()
    
    def verify(self, message, expected_hmac):
        """
        Verify HMAC for a message.
        
        Args:
            message: bytes - message to verify
            expected_hmac: bytes or hex string - expected HMAC value
        
        Returns:
            bool: True if HMAC matches, False otherwise
        """
        if isinstance(expected_hmac, str):
            expected_hmac = bytes.fromhex(expected_hmac)
        
        computed_hmac = self.compute(message)
        return computed_hmac == expected_hmac
    
    def verify_file(self, filepath, expected_hmac, chunk_size=8192):
        """
        Verify HMAC for a file.
        
        Args:
            filepath: string - path to file
            expected_hmac: bytes or hex string - expected HMAC value
            chunk_size: int - size of chunks to read
        
        Returns:
            bool: True if HMAC matches, False otherwise
        """
        if isinstance(expected_hmac, str):
            expected_hmac = bytes.fromhex(expected_hmac)
        
        computed_hmac = self.compute_file(filepath, chunk_size)
        return computed_hmac == expected_hmac


def hmac_sha256(key, message):
    """Convenience function for HMAC-SHA256."""
    hmac = HMAC(key, 'sha256')
    return hmac.compute(message)


def hmac_sha256_hex(key, message):
    """Convenience function for HMAC-SHA256 returning hex string."""
    hmac = HMAC(key, 'sha256')
    return hmac.compute_hex(message)