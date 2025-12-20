# CryptoCore

Программа для шифрования и расшифровки файлов с помощью AES-128 ECB.

## Быстрый старт

```bash
# Установи зависимости
pip install pycryptodome

# Установи программу
pip install -e .

# Создай тестовый файл
echo "Привет, мир!" > тест.txt

# Зашифруй
cd C:\Users\ewfrols\Desktop\crypto\m1\CryptoCore
python run.py --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input test.txt

# Расшифруй
python run.py --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input test.txt.enc