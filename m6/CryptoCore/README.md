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

##  **Спринт 5: Message Authentication Codes (HMAC)**

###  **Цель спринта**
Реализация функций для обеспечения аутентичности и целостности данных с помощью HMAC.

###  **Что было реализовано**

#### 1. **HMAC (Hash-based Message Authentication Code)**
- Реализация "с нуля" по стандарту **RFC 2104**
- Использует SHA-256 из спринта 4 в качестве хэш-функции
- Поддержка ключей произвольной длины
- Обработка файлов чанками для работы с большими файлами

#### 2. **Расширение CLI команды `dgst`**
```bash
# Генерация HMAC
cryptocore dgst --algorithm sha256 --hmac --key 0011223344556677 --input file.txt

# Проверка HMAC
cryptocore dgst --algorithm sha256 --hmac --key 0011223344556677 --input file.txt --verify hmac.txt

# Сохранение HMAC в файл
cryptocore dgst --algorithm sha256 --hmac --key 0011223344556677 --input file.txt --output hmac.txt


##  Быстрый старт (если основной пакет не установлен)

Если команда `cryptocore` не работает, используйте альтернативные скрипты:

### Вариант 1: Единый CLI скрипт
```bash
# Обычное хэширование
python cryptocore_cli.py dgst --algorithm sha256 --input file.txt

# Генерация HMAC
python cryptocore_cli.py dgst --algorithm sha256 --hmac --key 0011223344556677 --input file.txt

# Проверка HMAC
python cryptocore_cli.py dgst --algorithm sha256 --hmac --key 0011223344556677 --input file.txt --verify hmac.txt
Вариант 2: Только HMAC
bash
python cryptocore_hmac.py --key 0011223344556677 --input file.txt
python cryptocore_hmac.py --key 0011223344556677 --input file.txt --output hmac.txt
python cryptocore_hmac.py --key 0011223344556677 --input file.txt --verify hmac.txt

```bash
# 1. Полный тест
python test_full_functionality.py

# 2. Пример использования
echo "Hello, CryptoCore!" > message.txt
python cryptocore_cli.py dgst --algorithm sha256 --hmac --key 0011223344556677 --input message.txt
python cryptocore_cli.py dgst --algorithm sha256 --hmac --key 0011223344556677 --input message.txt --output message.hmac
python cryptocore_cli.py dgst --algorithm sha256 --hmac --key 0011223344556677 --input message.txt --verify message.hmac

# 3. Проверка обнаружения изменений
echo "TAMPERED" >> message.txt
python cryptocore_cli.py dgst --algorithm sha256 --hmac --key 0011223344556677 --input message.txt --verify message.hmac
# Должна быть ошибка

СПРИНТ 6
# Все функции доступны через:
python cryptocore_simple.py [команды]

# Полная демонстрация:
python final_demo.py
БОЛЬШЕ ИНФОРМАЦИИ В FINAL_REPORT.md


