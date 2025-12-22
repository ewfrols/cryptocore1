import struct
import binascii

class SHA256:
    def __init__(self):
        # Initialize hash values
        self.h = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
        
        # Initialize round constants
        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
        
        self.data = bytearray()
        self.bit_length = 0
    
    def _right_rotate(self, x, n):
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF
    
    def _process_block(self, block):
        """Process a 512-bit block."""
        # Prepare message schedule
        w = list(struct.unpack('>16I', block))
        
        # Extend the first 16 words into the remaining 48 words
        for i in range(16, 64):
            s0 = (self._right_rotate(w[i-15], 7) ^ 
                  self._right_rotate(w[i-15], 18) ^ 
                  (w[i-15] >> 3))
            s1 = (self._right_rotate(w[i-2], 17) ^ 
                  self._right_rotate(w[i-2], 19) ^ 
                  (w[i-2] >> 10))
            w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = self.h
        
        # Compression function main loop
        for i in range(64):
            s1 = self._right_rotate(e, 6) ^ self._right_rotate(e, 11) ^ self._right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + s1 + ch + self.k[i] + w[i]) & 0xFFFFFFFF
            
            s0 = self._right_rotate(a, 2) ^ self._right_rotate(a, 13) ^ self._right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & 0xFFFFFFFF
            
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        
        # Add compressed chunk to current hash value
        self.h[0] = (self.h[0] + a) & 0xFFFFFFFF
        self.h[1] = (self.h[1] + b) & 0xFFFFFFFF
        self.h[2] = (self.h[2] + c) & 0xFFFFFFFF
        self.h[3] = (self.h[3] + d) & 0xFFFFFFFF
        self.h[4] = (self.h[4] + e) & 0xFFFFFFFF
        self.h[5] = (self.h[5] + f) & 0xFFFFFFFF
        self.h[6] = (self.h[6] + g) & 0xFFFFFFFF
        self.h[7] = (self.h[7] + h) & 0xFFFFFFFF
    
    def update(self, data):
        """Update hash with data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.data.extend(data)
        self.bit_length += len(data) * 8
        
        # Process full blocks
        while len(self.data) >= 64:
            self._process_block(bytes(self.data[:64]))
            del self.data[:64]
    
    def digest(self):
        """Return final hash value."""
        # Make a copy to avoid modifying internal state
        data_copy = bytearray(self.data)
        bit_length_copy = self.bit_length
        
        # Padding
        data_copy.append(0x80)
        while (len(data_copy) % 64) != 56:
            data_copy.append(0x00)
        
        # Append bit length
        data_copy.extend(struct.pack('>Q', bit_length_copy))
        
        # Process final blocks
        h_backup = self.h.copy()
        
        for i in range(0, len(data_copy), 64):
            self._process_block(bytes(data_copy[i:i+64]))
        
        # Get result
        result = struct.pack('>8I', *self.h)
        
        # Restore state
        self.h = h_backup
        
        return result
    
    def hexdigest(self):
        """Return hash as hexadecimal string."""
        return binascii.hexlify(self.digest()).decode()
    
    def hash(self, data):
        """Quick hash data."""
        self.update(data)
        return self.hexdigest()
    
    def hash_file(self, filepath, chunk_size=8192):
        """Hash file in chunks."""
        import os
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Reset for new file
        self.__init__()
        
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                self.update(chunk)
        
        return self.hexdigest()


# Альтернативная простая версия через hashlib для сравнения
import hashlib

class SimpleSHA256:
    """Simple wrapper around hashlib for comparison."""
    def __init__(self):
        self.hasher = hashlib.sha256()
    
    def update(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.hasher.update(data)
    
    def hexdigest(self):
        return self.hasher.hexdigest()
    
    def hash_file(self, filepath, chunk_size=8192):
        import os
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        self.hasher = hashlib.sha256()  # Reset
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                self.update(chunk)
        
        return self.hexdigest()