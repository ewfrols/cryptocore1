# CryptoCore Sprint 6 - ФИНАЛЬНЫЙ ОТЧЕТ

##  ОБЗОР ПРОЕКТА
**CryptoCore** - образовательный криптографический проект с полной реализацией "с нуля" на Python.
Проект прошел 6 спринтов, каждый добавлял новую функциональность.

##  РЕАЛИЗОВАННЫЕ СПРИНТЫ

### Спринт 4: Хэш-функции
-  SHA-256 реализован с нуля по NIST FIPS 180-4
-  SHA3-256 через hashlib
-  Все NIST тестовые векторы пройдены

### Спринт 5: Message Authentication Codes (HMAC)
-  HMAC-SHA256 реализован с нуля по RFC 2104
-  Поддержка ключей произвольной длины
-  Все тестовые векторы RFC 4231 пройдены

### Спринт 6: Authenticated Encryption (GCM)
-  GCM (Galois/Counter Mode) реализован с нуля по NIST SP 800-38D
-  Умножение в поле Галуа GF(2¹²⁸)
-  Encrypt-then-MAC парадигма
-  Поддержка Associated Authenticated Data (AAD)
-  Катастрофический отказ при ошибке аутентификации

##  КЛЮЧЕВЫЕ ФАЙЛЫ

### Основная реализация:
- `cryptocore/crypto/hash/sha256_final.py` - SHA-256
- `cryptocore/crypto/mac/hmac.py` - HMAC-SHA256  
- `cryptocore/modes/gcm.py` - GCM режим

### CLI интерфейс:
- `cryptocore_simple.py` - Основной интерфейс командной строки

### Тестирование:
- `tests/test_hmac.py` - Тесты HMAC (13 тестов, все проходят)
- `tests/test_gcm.py` - Тесты GCM (11 тестов, все проходят)
- `final_test.py` - Полный функциональный тест

##  ИСПОЛЬЗОВАНИЕ

### Хэширование:
```bash
python cryptocore_simple.py dgst --algorithm sha256 --input file.txt

HMAC:# Генерация
python cryptocore_simple.py dgst --algorithm sha256 --hmac --key KEY --input file.txt

# Проверка
python cryptocore_simple.py dgst --algorithm sha256 --hmac --key KEY --input file.txt --verify hmac.txt

GCM шифрование:
# Шифрование (AAD может быть hex или текст)
python cryptocore_simple.py gcm --encrypt --key 00112233445566778899aabbccddeeff --aad "my data" --input file.txt

# Дешифрование
python cryptocore_simple.py gcm --decrypt --key 00112233445566778899aabbccddeeff --aad "my data" --input file.enc



# Все функции доступны через:
python cryptocore_simple.py [команды]

# Полная демонстрация:
python final_demo.py