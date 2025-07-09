@echo off
:: Активируем виртуальное окружение (для Windows)
call lib\Scripts\activate.bat

:: Переходим в папку core
cd core

:: Запускаем скрипт
python Helper.py

:: Закрываем BAT-файл (если не нужен pause)
exit