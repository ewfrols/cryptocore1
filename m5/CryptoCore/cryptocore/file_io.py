import os
from pathlib import Path

def read_file(file_path, binary=True):
    """Read file content."""
    mode = 'rb' if binary else 'r'
    try:
        with open(file_path, mode) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")

def write_file(file_path, data, binary=True):
    """Write data to file."""
    mode = 'wb' if binary else 'w'
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    try:
        with open(file_path, mode) as f:
            f.write(data)
        return True
    except IOError as e:
        raise IOError(f"Error writing file {file_path}: {str(e)}")

def read_file_in_chunks(file_path, chunk_size=8192):
    """Read file in chunks (generator)."""
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")

def compute_hash(file_path, algorithm='sha256', chunk_size=8192):
    """Compute hash of a file using specified algorithm."""
    from cryptocore.crypto.hash import SHA256, SHA3_256
    
    if algorithm.lower() in ['sha256', 'sha-256']:
        hasher = SHA256()
    elif algorithm.lower() in ['sha3-256', 'sha3_256']:
        hasher = SHA3_256()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    return hasher.hash_file(file_path, chunk_size)