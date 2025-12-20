#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обработка Initialization Vector (IV)
"""
import os
import struct


class ОбработчикIV:
    """Генерация и обработка IV"""
    
    РАЗМЕР_IV = 16  # 16 байт для AES
    
    @staticmethod
    def сгенерировать_iv() -> bytes:
        """Генерирует криптографически безопасный IV"""
        return os.urandom(ОбработчикIV.РАЗМЕР_IV)
    
    @staticmethod
    def добавить_iv_к_данным(iv: bytes, данные: bytes) -> bytes:
        """Добавляет IV в начало данных"""
        return iv + данные
    
    @staticmethod
    def извлечь_iv_из_данных(данные: bytes):
        """Извлекает IV из начала данных"""
        if len(данные) < ОбработчикIV.РАЗМЕР_IV:
            raise ValueError(f"Данные слишком короткие для IV. Минимум {ОбработчикIV.РАЗМЕР_IV} байт")
        
        iv = данные[:ОбработчикIV.РАЗМЕР_IV]
        остальные_данные = данные[ОбработчикIV.РАЗМЕР_IV:]
        return iv, остальные_данные
    
    @staticmethod
    def преобразовать_iv_в_hex(iv: bytes) -> str:
        """Преобразует IV в hex строку"""
        return iv.hex()
    
    @staticmethod
    def преобразовать_hex_в_iv(iv_hex: str) -> bytes:
        """Преобразует hex строку в IV"""
        return bytes.fromhex(iv_hex)