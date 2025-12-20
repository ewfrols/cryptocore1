#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой инициализационный файл для modes
Динамически загружает режимы чтобы избежать проблем с импортами
"""

import os
import sys
import importlib.util

class ФабрикаРежимов:
    """Фабрика для создания объектов режимов шифрования"""
    
    @staticmethod
    def создать_режим(название_режима: str, ключ: str):
        """
        Создает объект режима шифрования
        
        Args:
            название_режима: 'ecb', 'cbc', 'cfb', 'ofb', 'ctr'
            ключ: Ключ шифрования в hex
            
        Returns:
            Объект режима шифрования
        """
        # Список доступных режимов и их классов
        режимы = {
            'ecb': 'ECBMode',
            'cbc': 'CBCMode', 
            'cfb': 'CFBMode',
            'ofb': 'OFBMode',
            'ctr': 'CTRMode',
        }
        
        if название_режима not in режимы:
            raise ValueError(f"Неизвестный режим: {название_режима}. Доступно: {', '.join(режимы.keys())}")
        
        имя_класса = режимы[название_режима]
        
        # Путь к файлу режима
        текущая_папка = os.path.dirname(os.path.abspath(__file__))
        файл_режима = os.path.join(текущая_папка, f"{название_режима}.py")
        
        if not os.path.exists(файл_режима):
            raise FileNotFoundError(f"Файл режима не найден: {файл_режима}")
        
        # Динамически загружаем модуль
        spec = importlib.util.spec_from_file_location(f"{название_режима}_mode", файл_режима)
        модуль_режима = importlib.util.module_from_spec(spec)
        
        # Добавляем нужные импорты в пространство имен модуля
        модуль_режима.__dict__.update({
            'AESCore': None,  # Будет установлено позже
            'BaseMode': None, # Будет установлено позже
        })
        
        # Загружаем модуль
        spec.loader.exec_module(модуль_режима)
        
        # Теперь импортируем зависимости
        try:
            # BaseMode
            base_mode_path = os.path.join(текущая_папка, 'base_mode.py')
            if os.path.exists(base_mode_path):
                spec_base = importlib.util.spec_from_file_location("base_mode", base_mode_path)
                модуль_base = importlib.util.module_from_spec(spec_base)
                spec_base.loader.exec_module(модуль_base)
                модуль_режима.BaseMode = модуль_base.BaseMode
            
            # AESCore
            crypto_dir = os.path.dirname(текущая_папка)
            aes_core_path = os.path.join(crypto_dir, 'crypto', 'aes_core.py')
            if os.path.exists(aes_core_path):
                spec_aes = importlib.util.spec_from_file_location("aes_core", aes_core_path)
                модуль_aes = importlib.util.module_from_spec(spec_aes)
                spec_aes.loader.exec_module(модуль_aes)
                модуль_режима.AESCore = модуль_aes.AESCore
            
        except Exception as e:
            print(f"Предупреждение: не удалось загрузить зависимости: {e}")
        
        # Создаем объект
        if hasattr(модуль_режима, имя_класса):
            КлассРежима = getattr(модуль_режима, имя_класса)
            return КлассРежима(ключ)
        else:
            # Ищем любой класс с 'Mode' в конце
            for attr_name in dir(модуль_режима):
                if attr_name.endswith('Mode'):
                    КлассРежима = getattr(модуль_режима, attr_name)
                    return КлассРежима(ключ)
            
            raise AttributeError(f"В модуле {файл_режима} не найден класс режима")

# Экспортируем только фабрику
__all__ = ['ФабрикаРежимов']