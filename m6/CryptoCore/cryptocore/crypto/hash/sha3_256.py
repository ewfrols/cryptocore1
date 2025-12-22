import hashlib

class SHA3_256:
    """SHA3-256 implementation using Python's hashlib."""
    
    def __init__(self):
        self.hasher = hashlib.sha3_256()
    
    def update(self, data):
        """Update the hash with new data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.hasher.update(data)
    
    def digest(self):
        """Return the final hash digest."""
        return self.hasher.digest()
    
    def hexdigest(self):
        """Return the final hash as hexadecimal string."""
        return self.hasher.hexdigest()
    
    def hash_file(self, filepath, chunk_size=8192):
        """Hash a file in chunks."""
        import os
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                self.update(chunk)
        
        return self.hexdigest()