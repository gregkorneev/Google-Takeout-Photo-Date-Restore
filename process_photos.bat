@echo off
chcp 65001 > nul
echo.
echo ============================================
echo      Запуск обработки фото и JSON файлов
echo ============================================
echo.

:: Правильно обрабатываем путь, убираем лишний слэш
set "folder=%~dp0"
set "folder=%folder:~0,-1%"

:: Запускаем Python, путь уже чистый
"C:\Users\korne\AppData\Local\Programs\Python\Python313\python.exe" update_dates.py "%folder%"

echo.
echo ============================================
echo             Готово! Нажмите любую клавишу для выхода.
echo ============================================
pause
