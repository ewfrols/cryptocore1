import hashlib

class SimpleSHA256:
    """Простая обертка вокруг hashlib для тестирования CLI."""
    
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
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                self.update(chunk)
        
        return self.hexdigest()