#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест исправленного GCM
"""

import os
import sys

# Добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gcm_simple():
    """Простой тест GCM"""
    print("🧪 Простой тест GCM...")
    
    try:
        from cryptocore.modes.gcm import GCM
        
        # Простой тест
        key = bytes.fromhex("00000000000000000000000000000000")
        nonce = bytes.fromhex("000000000000000000000000")
        plaintext = b"Hello, GCM!"
        aad = b"authenticated but not encrypted"
        
        print(f"   Ключ: {key.hex()}")
        print(f"   Nonce: {nonce.hex()}")
        print(f"   Plaintext: {plaintext}")
        print(f"   AAD: {aad}")
        
        # Шифрование
        gcm = GCM(key)
        ciphertext, tag = gcm.encrypt(nonce, plaintext, aad)
        
        print(f"   Ciphertext: {ciphertext.hex()}")
        print(f"   Tag: {tag.hex()}")
        
        # Дешифрование
        gcm2 = GCM(key)
        decrypted = gcm2.decrypt(nonce, ciphertext, tag, aad)
        
        print(f"   Decrypted: {decrypted}")
        
        if decrypted == plaintext:
            print("✅ GCM тест пройден!")
            return True
        else:
            print("❌ Дешифрование не совпадает!")
            return False
    
    except Exception as e:
        print(f"❌ Ошибка GCM: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gcm_with_hex():
    """Тест GCM с hex строками"""
    print("\n🧪 Тест GCM с hex строками...")
    
    try:
        from cryptocore.modes.gcm import GCM
        
        key_hex = "00112233445566778899aabbccddeeff"
        key = bytes.fromhex(key_hex)
        
        # Генерируем случайный nonce
        nonce = os.urandom(12)
        
        plaintext = b"Hello, GCM! This is a test message."
        aad = bytes.fromhex("aabbcc")
        
        print(f"   Ключ (hex): {key_hex}")
        print(f"   Nonce: {nonce.hex()}")
        print(f"   Plaintext: {plaintext}")
        print(f"   AAD (hex): aabbcc")
        
        # Шифрование
        gcm = GCM(key)
        ciphertext, tag = gcm.encrypt(nonce, plaintext, aad)
        
        print(f"   Ciphertext длина: {len(ciphertext)} байт")
        print(f"   Tag: {tag.hex()}")
        
        # Дешифрование
        gcm2 = GCM(key)
        decrypted = gcm2.decrypt(nonce, ciphertext, tag, aad)
        
        print(f"   Decrypted: {decrypted}")
        
        if decrypted == plaintext:
            print("✅ GCM с hex тест пройден!")
            return True
        else:
            print("❌ Дешифрование не совпадает!")
            return False
    
    except Exception as e:
        print(f"❌ Ошибка GCM с hex: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция тестирования"""
    print("=" * 60)
    print("ИСПРАВЛЕННЫЙ GCM ТЕСТ")
    print("=" * 60)
    
    test1 = test_gcm_simple()
    test2 = test_gcm_with_hex()
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    
    if test1 and test2:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\nТеперь можно использовать cryptocore_simple.py:")
        print("  python cryptocore_simple.py gcm --encrypt --key 001122...")
        print("  python cryptocore_simple.py gcm --decrypt --key 001122...")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
    
    print("=" * 60)

if __name__ == "__main__":
    main()