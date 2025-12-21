#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенная версия CryptoCore в одном файле с поддержкой ВСЕХ режимов
"""
import os
import sys
import argparse
from Crypto.Cipher import AES

class SimpleCryptoCore:
    """Полная реализация всех режимов AES-128 в одном классе"""
    
    def __init__(self):
        self.block_size = 16
    
    def pad(self, data, mode):
        """PKCS#7 padding только для ECB и CBC"""
        if mode in ['ecb', 'cbc']:
            padding_len = self.block_size - (len(data) % self.block_size)
            if padding_len == 0:
                padding_len = self.block_size
            return data + bytes([padding_len] * padding_len)
        return data  # Без padding для потоковых режимов
    
    def unpad(self, data, mode):
        """Remove PKCS#7 padding"""
        if mode in ['ecb', 'cbc']:
            if len(data) == 0:
                return data
            padding_len = data[-1]
            if padding_len > self.block_size:
                return data  # Неверный padding, возвращаем как есть
            return data[:-padding_len]
        return data
    
    def xor_bytes(self, a, b):
        """XOR двух байтовых строк"""
        return bytes(x ^ y for x, y in zip(a, b))
    
    def encrypt(self, mode, key_hex, data, iv_hex=None):
        """Шифрование во всех режимах"""
        key = bytes.fromhex(key_hex)
        
        if mode == 'ecb':
            # ECB - самый простой
            data_padded = self.pad(data, 'ecb')
            cipher = AES.new(key, AES.MODE_ECB)
            return cipher.encrypt(data_padded)
        
        elif mode == 'cbc':
            # CBC с IV
            if iv_hex is None:
                iv = os.urandom(16)  # Генерируем IV
            else:
                iv = bytes.fromhex(iv_hex)
            
            data_padded = self.pad(data, 'cbc')
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted = b''
            prev_block = iv
            
            for i in range(0, len(data_padded), self.block_size):
                block = data_padded[i:i + self.block_size]
                block_to_encrypt = self.xor_bytes(block, prev_block)
                encrypted_block = cipher.encrypt(block_to_encrypt)
                encrypted += encrypted_block
                prev_block = encrypted_block
            
            if iv_hex is None:
                return iv + encrypted  # Возвращаем IV + данные
            else:
                return encrypted
        
        elif mode == 'cfb':
            # CFB (Cipher Feedback) - потоковый режим
            if iv_hex is None:
                iv = os.urandom(16)
            else:
                iv = bytes.fromhex(iv_hex)
            
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted = b''
            shift_register = iv  # Начинаем с IV
            
            # Обрабатываем данные блоками
            for i in range(0, len(data), self.block_size):
                # Шифруем текущее значение регистра сдвига
                encrypted_register = cipher.encrypt(shift_register)
                
                # Берем текущий блок данных
                current_block = data[i:min(i + self.block_size, len(data))]
                
                # XOR шифрованного регистра с данными
                if len(current_block) < self.block_size:
                    # Для последнего неполного блока используем только нужные байты
                    keystream = encrypted_register[:len(current_block)]
                else:
                    keystream = encrypted_register
                
                encrypted_block = self.xor_bytes(current_block, keystream)
                encrypted += encrypted_block
                
                # Обновляем регистр сдвига
                # В CFB регистр обновляется зашифрованными данными
                shift_register = encrypted_block.ljust(self.block_size, b'\x00')
            
            if iv_hex is None:
                return iv + encrypted
            else:
                return encrypted
        
        elif mode == 'ofb':
            # OFB (Output Feedback) - потоковый режим
            if iv_hex is None:
                iv = os.urandom(16)
            else:
                iv = bytes.fromhex(iv_hex)
            
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted = b''
            shift_register = iv  # Начинаем с IV
            
            # Генерируем ключевой поток
            keystream = b''
            while len(keystream) < len(data):
                # Шифруем текущее значение регистра
                encrypted_register = cipher.encrypt(shift_register)
                keystream += encrypted_register
                shift_register = encrypted_register  # Обновляем регистр
            
            # Обрезаем ключевой поток до нужной длины
            keystream = keystream[:len(data)]
            
            # XOR ключевого потока с данными
            encrypted = self.xor_bytes(data, keystream)
            
            if iv_hex is None:
                return iv + encrypted
            else:
                return encrypted
        
        elif mode == 'ctr':
            # CTR (Counter) - потоковый режим
            if iv_hex is None:
                # Используем IV как nonce (первые 12 байт) + счетчик (последние 4 байта)
                nonce = os.urandom(12)
                counter = 0
            else:
                # Если IV указан, используем его как nonce
                iv_bytes = bytes.fromhex(iv_hex)
                if len(iv_bytes) >= 12:
                    nonce = iv_bytes[:12]
                else:
                    nonce = iv_bytes.ljust(12, b'\x00')
                counter = 0
            
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted = b''
            
            # Вычисляем сколько блоков нужно
            blocks_needed = (len(data) + self.block_size - 1) // self.block_size
            
            for i in range(blocks_needed):
                # Создаем значение счетчика: nonce + counter
                counter_bytes = i.to_bytes(4, 'big')
                counter_value = nonce + counter_bytes
                
                # Шифруем значение счетчика
                keystream_block = cipher.encrypt(counter_value)
                
                # Берем текущий блок данных
                start_idx = i * self.block_size
                end_idx = min(start_idx + self.block_size, len(data))
                current_block = data[start_idx:end_idx]
                
                # XOR с ключевым потоком
                if len(current_block) < self.block_size:
                    keystream = keystream_block[:len(current_block)]
                else:
                    keystream = keystream_block
                
                encrypted_block = self.xor_bytes(current_block, keystream)
                encrypted += encrypted_block
            
            if iv_hex is None:
                # Возвращаем nonce + зашифрованные данные
                return nonce + encrypted
            else:
                return encrypted
        
        else:
            raise ValueError(f"Неизвестный режим: {mode}")
    
    def decrypt(self, mode, key_hex, data, iv_hex=None):
        """Расшифровка во всех режимах"""
        key = bytes.fromhex(key_hex)
        
        if mode == 'ecb':
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted = cipher.decrypt(data)
            return self.unpad(decrypted, 'ecb')
        
        elif mode == 'cbc':
            if iv_hex is None:
                # IV в начале данных
                iv = data[:16]
                data = data[16:]
            else:
                iv = bytes.fromhex(iv_hex)
            
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted = b''
            prev_block = iv
            
            for i in range(0, len(data), self.block_size):
                block = data[i:i + self.block_size]
                decrypted_block = cipher.decrypt(block)
                original_block = self.xor_bytes(decrypted_block, prev_block)
                decrypted += original_block
                prev_block = block
            
            return self.unpad(decrypted, 'cbc')
        
        elif mode == 'cfb':
            # CFB (Cipher Feedback) - расшифровка
            if iv_hex is None:
                # IV в начале данных
                iv = data[:16]
                data = data[16:]
            else:
                iv = bytes.fromhex(iv_hex)
            
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted = b''
            shift_register = iv  # Начинаем с IV
            
            # Обрабатываем данные блоками
            for i in range(0, len(data), self.block_size):
                # Шифруем текущее значение регистра сдвига
                encrypted_register = cipher.encrypt(shift_register)
                
                # Берем текущий блок зашифрованных данных
                current_block = data[i:min(i + self.block_size, len(data))]
                
                # XOR шифрованного регистра с зашифрованными данными
                if len(current_block) < self.block_size:
                    # Для последнего неполного блока используем только нужные байты
                    keystream = encrypted_register[:len(current_block)]
                else:
                    keystream = encrypted_register
                
                decrypted_block = self.xor_bytes(current_block, keystream)
                decrypted += decrypted_block
                
                # КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ:
                # В CFB при расшифровке регистр обновляется ВХОДНЫМИ ДАННЫМИ (ciphertext)
                shift_register = current_block.ljust(self.block_size, b'\x00')
            
            return decrypted
        
        elif mode == 'ofb':
            # В OFB расшифровка симметрична шифрованию
            if iv_hex is None:
                # Nonce в начале данных
                nonce = data[:16]
                data = data[16:]
                return self.encrypt('ofb', key_hex, data, nonce.hex())
            else:
                return self.encrypt('ofb', key_hex, data, iv_hex)
        
        elif mode == 'ctr':
            # В CTR расшифровка симметрична шифрованию
            if iv_hex is None:
                # Nonce в начале данных
                if len(data) < 12:
                    raise ValueError("Данные слишком короткие для nonce")
                nonce = data[:12]
                data = data[12:]
                return self.encrypt('ctr', key_hex, data, nonce.hex())
            else:
                return self.encrypt('ctr', key_hex, data, iv_hex)
        
        else:
            raise ValueError(f"Неизвестный режим: {mode}")

def main():
    parser = argparse.ArgumentParser(description='CryptoCore Simple - все режимы в одном файле')
    parser.add_argument('--algorithm', required=True, choices=['aes'])
    parser.add_argument('--mode', required=True, choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'])
    parser.add_argument('--encrypt', action='store_true')
    parser.add_argument('--decrypt', action='store_true')
    parser.add_argument('--key', required=True, help='32 hex символа')
    parser.add_argument('--iv', help='Initialization vector')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output')
    
    args = parser.parse_args()
    
    # Проверки
    if not args.encrypt and not args.decrypt:
        print("Ошибка: укажите --encrypt или --decrypt")
        return
    
    if len(args.key) != 32:
        print(f"Ошибка: ключ должен быть 32 символа, а не {len(args.key)}")
        return
    
    # Читаем файл
    if not os.path.exists(args.input):
        print(f"Ошибка: файл {args.input} не найден")
        return
    
    with open(args.input, 'rb') as f:
        data = f.read()
    
    if len(data) == 0:
        print("Предупреждение: файл пустой")
    
    # Создаем обработчик
    crypto = SimpleCryptoCore()
    
    # Определяем выходной файл
    if args.output:
        output_file = args.output
    elif args.encrypt:
        output_file = args.input + '.enc'
    else:
        output_file = args.input + '.dec'
    
    # Выполняем операцию
    try:
        if args.encrypt:
            result = crypto.encrypt(args.mode, args.key, data, args.iv)
            print(f"Успешно! Результат в {output_file}")
            print(f"Размер: {len(data)} -> {len(result)} байт")
            
            if args.mode in ['cbc', 'cfb', 'ofb', 'ctr'] and args.iv is None:
                print(f"IV/nonce сгенерирован и сохранен в начале файла")
                
        else:
            result = crypto.decrypt(args.mode, args.key, data, args.iv)
            print(f"Успешно! Результат в {output_file}")
            print(f"Размер: {len(data)} -> {len(result)} байт")
        
        # Записываем результат
        with open(output_file, 'wb') as f:
            f.write(result)
        
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("CRYPTOCORE SIMPLE - полная поддержка всех режимов")
    print("Режимы: ECB, CBC, CFB, OFB, CTR")
    print("=" * 60)
    main()