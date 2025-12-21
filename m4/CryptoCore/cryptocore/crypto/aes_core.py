#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Общая логика AES для всех режимов
"""
from Crypto.Cipher import AES


class AESCore:
    """Базовый класс для работы с AES"""
    
    БЛОК_РАЗМЕР = 16  # Размер блока AES
    КЛЮЧ_РАЗМЕР = 16  # Размер ключа AES-128
    
    @staticmethod
    def создать_шифрователь(ключ_hex: str):
        """Создает шифрователь AES"""
        ключ_байты = bytes.fromhex(ключ_hex)
        
        if len(ключ_байты) != AESCore.КЛЮЧ_РАЗМЕР:
            raise ValueError(f"Ключ должен быть {AESCore.КЛЮЧ_РАЗМЕР} байт для AES-128")
        
        return AES.new(ключ_байты, AES.MODE_ECB)
    
    @staticmethod
    def шифровать_блок(шифрователь, блок: bytes) -> bytes:
        """Шифрует один блок"""
        if len(блок) != AESCore.БЛОК_РАЗМЕР:
            raise ValueError(f"Размер блока должен быть {AESCore.БЛОК_РАЗМЕР} байт")
        return шифрователь.encrypt(блок)
    
    @staticmethod
    def расшифровать_блок(шифрователь, блок: bytes) -> bytes:
        """Расшифровывает один блок"""
        if len(блок) != AESCore.БЛОК_РАЗМЕР:
            raise ValueError(f"Размер блока должен быть {AESCore.БЛОК_РАЗМЕР} байт")
        return шифрователь.decrypt(блок)