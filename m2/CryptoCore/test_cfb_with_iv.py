# test_cfb_with_iv.py
import subprocess
import os

ключ = '000102030405060708090a0b0c0d0e0f'
iv = '00112233445566778899aabbccddeeff'
файл = 'test.bin'

# Создаем тестовый файл
with open(файл, 'wb') as f:
    f.write(b'Test data for CFB with IV')

# 1. Шифруем с IV
print("1. Шифруем CFB с IV...")
команда = [
    'python', 'cryptocore_simple.py',
    '--algorithm', 'aes',
    '--mode', 'cfb',
    '--encrypt',
    '--key', ключ,
    '--iv', iv,  # ПЕРЕДАЕМ IV
    '--input', файл
]
результат = subprocess.run(команда, capture_output=True)
print(f"   Код возврата: {результат.returncode}")
print(f"   Вывод: {результат.stdout.decode('utf-8', errors='ignore')[:100]}")

if результат.returncode != 0:
    print(f"   Ошибка: {результат.stderr.decode('utf-8', errors='ignore')[:200]}")

# 2. Расшифровываем с ТАКИМ ЖЕ IV
print("\n2. Расшифровываем CFB с тем же IV...")
команда = [
    'python', 'cryptocore_simple.py',
    '--algorithm', 'aes',
    '--mode', 'cfb',
    '--decrypt',
    '--key', ключ,
    '--iv', iv,  # ТОЧНО ТАКОЙ ЖЕ IV
    '--input', файл + '.enc'
]
результат = subprocess.run(команда, capture_output=True)
print(f"   Код возврата: {результат.returncode}")

# Удаляем файлы
for f in [файл, файл + '.enc', файл + '.enc.dec']:
    if os.path.exists(f):
        os.remove(f)