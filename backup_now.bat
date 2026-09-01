@echo off
chcp 65001 >nul
echo [SkyBook] Dang backup database...
cd /d "e:\du an\Booking"
venv\Scripts\python.exe backup_db.py
echo.
echo Hoan thanh! File backup luu tai: db_backups\
pause