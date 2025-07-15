@echo off
REM Батник для швидкого запуску гри DropBox на Windows
chcp 65001 >nul

echo ================================================
echo           ЗАПУСК ГРИ DROPBOX
echo ================================================

REM Перевірка наявності Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python не знайдено в системі!
    echo   Завантажте Python з https://python.org
    pause
    exit /b 1
)

REM Перевірка наявності pygame
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Pygame не встановлено!
    echo   Встановлюємо pygame...
    pip install pygame
    if %errorlevel% neq 0 (
        echo ✗ Помилка встановлення pygame
        pause
        exit /b 1
    )
)

echo ✓ Всі залежності встановлені
echo Запуск гри...
echo.

REM Запуск гри
python run_game.py

REM Пауза після завершення
echo.
echo Гру завершено
pause
