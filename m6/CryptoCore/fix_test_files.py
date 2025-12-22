#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление тестовых файлов с русскими символами в байтовых строках
"""

import os
import re

def fix_file(filepath):
    """Исправить русские символы в байтовых строках"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Исправляем байтовые строки с русскими символами
    pattern = r'b["\']([^"\']*[а-яА-ЯёЁ][^"\']*)["\']'
    
    def replace_match(match):
        text = match.group(1)
        # Заменяем русский текст на английский
        replacements = {
            'Тестовые данные': 'Test data',
            'Тест интероперабельности': 'Interoperability test',
            'Привет мир': 'Hello world',
            'Тест интероперабельности': 'Interoperability test',
            'интероперабельности': 'interoperability',
            'Привет': 'Hello',
            'мир': 'world',
            'Тест': 'Test',
            'данные': 'data',
            'проверки': 'testing',
            'работы': 'work',
            'файлами': 'files',
            'файлы': 'files',
        }
        
        for ru, en in replacements.items():
            text = text.replace(ru, en)
        
        return f"b'{text}'"
    
    new_content = re.sub(pattern, replace_match, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Исправлен: {filepath}")
        return True
    
    return False

def main():
    """Основная функция"""
    print("Исправление тестовых файлов...")
    
    fixed_count = 0
    for root, dirs, files in os.walk('tests'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    fixed_count += 1
    
    print(f"Исправлено файлов: {fixed_count}")

if __name__ == "__main__":
    main()