"""
HMAC (Hash-based Message Authentication Code) implementation.

RFC 2104: HMAC: Keyed-Hashing for Message Authentication
"""

import hashlib
from ..hash.sha256_final import SHA256

class HMAC:
    """HMAC implementation supporting SHA-256."""
    
    def __init__(self, key, hash_algorithm='sha256'):
        """
        Initialize HMAC with key and hash algorithm.
        
        Args:
            key: bytes or str - secret key
            hash_algorithm: str - hash algorithm ('sha256' or 'sha3-256')
        """
        self.hash_algorithm = hash_algorithm
        
        # Convert key to bytes if it's a string
        if isinstance(key, str):
            # Try to interpret as hex first
            if len(key) % 2 == 0:
                try:
                    self.key = bytes.fromhex(key)
                except ValueError:
                    self.key = key.encode('utf-8')
            else:
                self.key = key.encode('utf-8')
        else:
            self.key = key
        
        # Block size for hash algorithm
        if hash_algorithm == 'sha256':
            self.block_size = 64  # SHA-256 block size
            self.hash_func = SHA256
        elif hash_algorithm == 'sha3-256':
            self.block_size = 136  # SHA3-256 rate
            # For simplicity, we'll use hashlib for SHA3
            self.hash_func = lambda: hashlib.sha3_256()
        else:
            raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
        
        # Prepare key
        self._prepare_key()
        
        # Initialize hash context
        self._init_hash()
    
    def _prepare_key(self):
        """Prepare the key according to RFC 2104."""
        # Ensure key is bytes
        if isinstance(self.key, str):
            self.key = self.key.encode('utf-8')
        
        if len(self.key) > self.block_size:
            # Hash key if it's too long
            if self.hash_algorithm == 'sha256':
                hash_obj = SHA256()
                hash_obj.update(self.key)
                self.key = hash_obj.digest()
            else:
                self.key = hashlib.sha3_256(self.key).digest()
        
        # Pad key with zeros if too short
        if len(self.key) < self.block_size:
            self.key = self.key.ljust(self.block_size, b'\x00')
        
        # Create inner and outer padded keys
        self.ipad = bytes(x ^ 0x36 for x in self.key)
        self.opad = bytes(x ^ 0x5C for x in self.key)
    
    def _init_hash(self):
        """Initialize hash context for new calculation."""
        if self.hash_algorithm == 'sha256':
            self.inner_hash = SHA256()
            self.outer_hash = SHA256()
        else:
            self.inner_hash = hashlib.sha3_256()
            self.outer_hash = hashlib.sha3_256()
        
        # Update inner hash with ipad
        self.inner_hash.update(self.ipad)
    
    def update(self, data):
        """
        Update HMAC with more data.
        
        Args:
            data: bytes - data to authenticate
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.inner_hash.update(data)
    
    def digest(self):
        """
        Return HMAC digest.
        
        Returns:
            bytes: HMAC digest
        """
        # Get inner hash result
        inner_digest = self.inner_hash.digest()
        
        # Compute outer hash
        self.outer_hash.update(self.opad)
        self.outer_hash.update(inner_digest)
        
        return self.outer_hash.digest()
    
    def hexdigest(self):
        """
        Return HMAC digest as hexadecimal string.
        
        Returns:
            str: HMAC digest in hex
        """
        return self.digest().hex()
    
    # Методы для совместимости с тестами
    def compute(self, data):
        """Compute HMAC for data (for test compatibility)."""
        # Reinitialize for new computation
        self._init_hash()
        self.update(data)
        return self.digest()
    
    def compute_hex(self, data):
        """Compute HMAC hex for data (for test compatibility)."""
        # Reinitialize for new computation
        self._init_hash()
        self.update(data)
        return self.hexdigest()
    
    def compute_file_hex(self, filepath, chunk_size=8192):
        """Compute HMAC hex for file (for test compatibility)."""
        # Reinitialize for new computation
        self._init_hash()
        
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                self.update(chunk)
        
        return self.hexdigest()
    
    def verify(self, data, expected_hmac):
        """
        Verify HMAC digest (for test compatibility).
        
        Args:
            data: bytes - data to verify
            expected_hmac: bytes or str - expected HMAC
        
        Returns:
            bool: True if HMAC matches
        """
        # Reinitialize for new computation
        self._init_hash()
        self.update(data)
        
        computed_hmac = self.digest()
        
        if isinstance(expected_hmac, str):
            expected_hmac = bytes.fromhex(expected_hmac)
        
        return self._constant_time_compare(computed_hmac, expected_hmac)
    
    def verify_digest(self, hmac_digest):
        """
        Verify HMAC digest (alternative method).
        
        Args:
            hmac_digest: bytes or str - HMAC digest to verify
        
        Returns:
            bool: True if digest matches
        """
        if isinstance(hmac_digest, str):
            hmac_digest = bytes.fromhex(hmac_digest)
        
        return self._constant_time_compare(self.digest(), hmac_digest)
    
    def _constant_time_compare(self, a, b):
        """Constant time comparison to prevent timing attacks."""
        if len(a) != len(b):
            return False
        
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        
        return result == 0