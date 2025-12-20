# test_sequential.py
import subprocess
import os
import time

def тест_последовательно():
    """Тестирует режимы последовательно с паузой"""
    ключ = '000102030405060708090a0b0c0d0e0f'
    iv = '00112233445566778899aabbccddeeff'
    
    with open('temp_test.txt', 'w') as f:
        f.write('Test data')
    
    for режим in ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']:
        print(f"\n=== Тестируем {режим.upper()} ===")
        
        # Удаляем старые файлы
        for f in ['temp_test.txt.enc', 'temp_test.txt.enc.dec']:
            if os.path.exists(f):
                os.remove(f)
        
        time.sleep(0.1)  # Пауза для системы
        
        # Шифруем
        команда = ['python', 'cryptocore_simple.py', '--algorithm', 'aes', 
                  '--mode', режим, '--encrypt', '--key', ключ, '--input', 'temp_test.txt']
        
        if режим in ['cbc', 'cfb', 'ofb']:
            команда.extend(['--iv', iv])
        
        print(f"Команда: {' '.join(команда)}")
        результат = subprocess.run(команда, capture_output=True)
        print(f"Шифрование: {'OK' if результат.returncode == 0 else 'FAIL'}")
        
        if результат.returncode != 0:
            print(f"Ошибка: {результат.stderr.decode()[:200]}")
            continue
        
        # Расшифровываем
        команда = ['python', 'cryptocore_simple.py', '--algorithm', 'aes',
                  '--mode', режим, '--decrypt', '--key', ключ, '--input', 'temp_test.txt.enc']
        
        if режим in ['cbc', 'cfb', 'ofb']:
            команда.extend(['--iv', iv])
        
        результат = subprocess.run(команда, capture_output=True)
        print(f"Расшифровка: {'OK' if результат.returncode == 0 else 'FAIL'}")
        
        # Сравниваем
        if os.path.exists('temp_test.txt') and os.path.exists('temp_test.txt.enc.dec'):
            with open('temp_test.txt', 'rb') as f1, open('temp_test.txt.enc.dec', 'rb') as f2:
                if f1.read() == f2.read():
                    print(f"✓ {режим.upper()} работает!")
                else:
                    print(f"✗ {режим.upper()} не работает")
        
        # Очистка
        for f in ['temp_test.txt.enc', 'temp_test.txt.enc.dec']:
            if os.path.exists(f):
                os.remove(f)
    
    os.remove('temp_test.txt')

тест_последовательно()