@echo off
echo ========================================
echo CryptoCore - File Encryption
echo ========================================
echo.

if "%1"=="" (
    echo Usage:
    echo   run.bat --algorithm aes --mode ecb --encrypt --key 000102... --input file.txt
    echo   run.bat --algorithm aes --mode ecb --decrypt --key 000102... --input file.enc
    echo.
    echo Example:
    echo   run.bat --algorithm aes --mode ecb --encrypt ^
    echo     --key 000102030405060708090a0b0c0d0e0f ^
    echo     --input "test.txt"
    echo.
    pause
    exit /b
)

echo Running CryptoCore...
echo.

python run.py %*

echo.
pause