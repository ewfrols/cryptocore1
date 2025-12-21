# CryptoCore - Шифрование файлов AES

Программа для шифрования и расшифровки файлов с поддержкой режимов:
- ECB (Electronic Codebook) - Sprint 1
- CBC (Cipher Block Chaining)
- CFB (Cipher Feedback)
- OFB (Output Feedback) 
- CTR (Counter)

## Установка

```bash
pip install pycryptodome
pip install -e .

Базовый синтаксис:
cryptocore --algorithm aes --mode MODE [--encrypt|--decrypt] --key KEY --input FILE [--output FILE] [--iv IV]

Режимы работы с IV:
Шифрование (IV генерируется автоматически):
# Для всех режимов кроме ECB
cryptocore --algorithm aes --mode cbc --encrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input plaintext.txt \
  --output ciphertext.bin

Расшифровка с IV:
# Вариант 1: IV указан явно
cryptocore --algorithm aes --mode cbc --decrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --iv aabbccddeeff00112233445566778899 \
  --input ciphertext.bin \
  --output decrypted.txt

# Вариант 2: IV читается из файла (первые 16 байт)
cryptocore --algorithm aes --mode cbc --decrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input ciphertext.bin \
  --output decrypted.txt

  Примеры для всех режимов:
  CBC:# Шифрование
cryptocore --algorithm aes --mode cbc --encrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input data.txt

# Расшифровка
cryptocore --algorithm aes --mode cbc --decrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input data.txt.enc

CFB, OFB, CTR (потоковые режимы без padding):
# Шифрование
cryptocore --algorithm aes --mode ctr --encrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input image.jpg \
  --output encrypted.jpg

# Расшифровка  
cryptocore --algorithm aes --mode ctr --decrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input encrypted.jpg \
  --output restored.jpg

Интероперабельность с OpenSSL
1. Шифрование CryptoCore → Расшифровка OpenSSL:
# Шифруем файл
cryptocore --algorithm aes --mode cbc --encrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input plain.txt \
  --output cipher.bin

# Извлекаем IV (первые 16 байт)
dd if=cipher.bin of=iv.bin bs=16 count=1
dd if=cipher.bin of=ciphertext_only.bin bs=16 skip=1

# Расшифровываем через OpenSSL
openssl enc -aes-128-cbc -d \
  -K 000102030405060708090a0b0c0d0e0f \
  -iv $(xxd -p iv.bin | tr -d '\n') \
  -in ciphertext_only.bin \
  -out decrypted.txt

Шифрование OpenSSL → Расшифровка CryptoCore:
# Шифруем через OpenSSL
openssl enc -aes-128-cbc \
  -K 000102030405060708090a0b0c0d0e0f \
  -iv aabbccddeeff00112233445566778899 \
  -in plain.txt \
  -out openssl_cipher.bin

# Расшифровываем через CryptoCore
cryptocore --algorithm aes --mode cbc --decrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --iv aabbccddeeff00112233445566778899 \
  --input openssl_cipher.bin \
  --output decrypted.txt

Тестирование:
# Запуск всех тестов
python -m pytest tests/

# Тестирование интероперабельности
python examples/interop_test.py



## Sprint 3: Криптографически безопасный генератор случайных чисел (CSPRNG)

### Новые возможности в Sprint 3

 **Автоматическая генерация ключей**  
Теперь при шифровании можно не указывать ключ! Программа сгенерирует криптографически безопасный случайный ключ и покажет его на экране.

 **Модуль CSPRNG**  
Реализован криптографически безопасный генератор случайных чисел на основе `os.urandom()`.

 **Улучшенная безопасность**  
Все случайные данные (ключи и IV) генерируются через CSPRNG.

 **Проверка слабых ключей**  
Программа предупреждает, если пользователь указывает слабый ключ.

### Использование новых функций

#### Шифрование с автоматической генерацией ключа
```bash
cryptocore --algorithm aes --mode cbc --encrypt --input документ.txt

Программа выведет:[INFO] Сгенерирован ключ: a1b2c3d4e5f678901234567890abcdef
✓ Шифрование завершено

ВАЖНО: Сохраните показанный ключ! Он понадобится для расшифровки.
ШИФРОВАНИЕ:
python -m cryptocore.main -a aes -m cbc -e --input test.txt --output new_encrypted.bin
РАСШИФРОВКА:
python -m cryptocore.main -a aes -m cbc -d --key ЗАПИСАННЫЙ_КЛЮЧ --input new_encrypted.bin --output decrypted.txt
ПРОВЕРКА: 
type test.txt
type decrypted.txt