#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Реализация режима ECB (Electronic Codebook)
"""

# Прямые импорты без относительных путей
import os
import sys

# Добавляем родительскую папку в путь для импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Пробуем импортировать через абсолютный путь
    from cryptocore.modes.base_mode import BaseMode
    from cryptocore.crypto.aes_core import AESCore
    print(f"DEBUG: Импорты успешны в ECB")
except ImportError as e:
    print(f"DEBUG: Ошибка импорта в ECB: {e}")
    # Fallback: импортируем напрямую из файлов
    import importlib.util
    
    # BaseMode
    base_mode_path = os.path.join(current_dir, 'base_mode.py')
    spec = importlib.util.spec_from_file_location("base_mode", base_mode_path)
    base_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base_module)
    BaseMode = base_module.BaseMode
    
    # AESCore  
    aes_core_path = os.path.join(parent_dir, 'crypto', 'aes_core.py')
    spec = importlib.util.spec_from_file_location("aes_core", aes_core_path)
    aes_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aes_module)
    AESCore = aes_module.AESCore


class ECBMode(BaseMode):
    """Режим Electronic Codebook"""
    
    def __init__(self, ключ: str):
        super().__init__(ключ)
        self.требует_дополнения = True
    
    def зашифровать(self, данные: bytes, iv: bytes = None) -> bytes:
        """
        Шифрование в режиме ECB
        """
        # Подготавливаем данные (добавляем padding)
        подготовленные_данные = self.подготовить_данные_для_шифрования(данные)
        
        # Шифруем блок за блоком
        зашифрованные_данные = b''
        
        for i in range(0, len(подготовленные_данные), AESCore.БЛОК_РАЗМЕР):
            блок = подготовленные_данные[i:i + AESCore.БЛОК_РАЗМЕР]
            зашифрованный_блок = AESCore.шифровать_блок(self.шифрователь, блок)
            зашифрованные_данные += зашифрованный_блок
        
        return зашифрованные_данные
    
    def расшифровать(self, данные: bytes, iv: bytes = None) -> bytes:
        """
        Расшифровка в режиме ECB
        """
        # Проверяем что данные кратны размеру блока
        if len(данные) % AESCore.БЛОК_РАЗМЕР != 0:
            raise ValueError(f"Данные должны быть кратны {AESCore.БЛОК_РАЗМЕР} байтам")
        
        # Расшифровываем блок за блоком
        расшифрованные_данные = b''
        
        for i in range(0, len(данные), AESCore.БЛОК_РАЗМЕР):
            блок = данные[i:i + AESCore.БЛОК_РАЗМЕР]
            расшифрованный_блок = AESCore.расшифровать_блок(self.шифрователь, блок)
            расшифрованные_данные += расшифрованный_блок
        
        # Удаляем padding
        return self.обработать_расшифрованные_данные(расшифрованные_данные)