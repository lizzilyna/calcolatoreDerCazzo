@echo off
:: Avvia Docker se non è in esecuzione
if not exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
    echo Installa Docker Desktop prima!
    pause
    exit
)
start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
timeout /t 10 >nul

:: Avvia l'app
cd /d "C:\Users\ACER\Desktop\python autodid\KO - Copia"
docker-compose up
start http://localhost:5000