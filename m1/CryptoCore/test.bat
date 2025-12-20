@echo off
echo ========================================
echo CryptoCore Test
echo ========================================
echo.

echo 1. Creating test file...
(
echo Hello World!
echo This is a test.
echo Testing encryption.
) > test.txt

echo.
echo 2. Encrypting file...
echo.
python run.py --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input test.txt

if not exist "test.txt.enc" (
    echo.
    echo ERROR: test.txt.enc not created!
    echo.
    pause
    exit /b 1
)

echo.
echo 3. Decrypting file...
echo.
python run.py --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input test.txt.enc

if not exist "test.txt.enc.dec" (
    echo.
    echo ERROR: test.txt.enc.dec not created!
    echo.
    pause
    exit /b 1
)

echo.
echo 4. Comparing files...
echo.
fc /b test.txt test.txt.enc.dec > nul
if errorlevel 1 (
    echo ERROR: Files are DIFFERENT!
) else (
    echo SUCCESS: Files are IDENTICAL!
)

echo.
echo 5. Cleaning up...
del test.txt 2>nul
del test.txt.enc 2>nul
del test.txt.enc.dec 2>nul

echo.
echo Test completed!
pause