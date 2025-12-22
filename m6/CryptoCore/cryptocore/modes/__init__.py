"""
Block cipher modes of operation.
"""

from .base_mode import BaseMode
from .ecb import ECB
from .cbc import CBC
from .cfb import CFB
from .ofb import OFB
from .ctr import CTR
from .gcm import GCM, AuthenticationError  # Добавлено для GCM

__all__ = [
    'BaseMode', 'ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'GCM', 'AuthenticationError'
]

# Mode registry for CLI
MODES = {
    'ecb': ECB,
    'cbc': CBC,
    'cfb': CFB,
    'ofb': OFB,
    'ctr': CTR,
    'gcm': GCM,  # Добавлено GCM
}