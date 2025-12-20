#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Базовый класс для всех режимов шифрования
"""
from abc import ABC, abstractmethod
from cryptocore.crypto.aes_core import AESCore
from cryptocore.crypto.padding import PKCS7Дополнение


class BaseMode(ABC):
    """Абстрактный базовый класс для режимов шифрования"""
    
    def __init__(self, ключ: str):
        self.ключ = ключ
        self.шифрователь = AESCore.создать_шифрователь(ключ)
        self.требует_дополнения = False
    
    @abstractmethod
    def зашифровать(self, данные: bytes, iv: bytes = None) -> bytes:
        """Шифрует данные"""
        pass
    
    @abstractmethod
    def расшифровать(self, данные: bytes, iv: bytes = None) -> bytes:
        """Расшифровывает данные"""
        pass
    
    def подготовить_данные_для_шифрования(self, данные: bytes) -> bytes:
        """Подготавливает данные для шифрования (добавляет padding если нужно)"""
        if self.требует_дополнения:
            return PKCS7Дополнение.добавить_дополнение(данные)
        return данные
    
    def обработать_расшифрованные_данные(self, данные: bytes) -> bytes:
        """Обрабатывает расшифрованные данные (удаляет padding если нужно)"""
        if self.требует_дополнения:
            результат = PKCS7Дополнение.удалить_дополнение(данные)
            if результат is None:
                raise ValueError("Неправильное дополнение в расшифрованных данных")
            return результат
        return данные
    
    @staticmethod
    def xor_блоков(блок1: bytes, блок2: bytes) -> bytes:
        """XOR двух блоков"""
        return bytes(a ^ b for a, b in zip(блок1, блок2))