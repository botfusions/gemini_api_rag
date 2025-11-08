@echo off
REM YouTube Kanal Analiz Araci - Calistirma Scripti (Windows)

echo.
echo ================================
echo YouTube Kanal Analiz Araci
echo ================================
echo.

REM .env kontrolu
if not exist ".env" (
    echo [HATA] .env dosyasi bulunamadi!
    echo.
    echo Lutfen once setup.bat scriptini calistirin:
    echo   setup.bat
    echo.
    pause
    exit /b 1
)

REM API anahtarlarinin girilip girilmedigini kontrol et
findstr /C:"your_apify_api_key_here" .env >nul
if not errorlevel 1 (
    echo [UYARI] API anahtarlari girilmemis!
    echo.
    echo .env dosyasini duzenleyip gercek API anahtarlarinizi ekleyin:
    echo   notepad .env
    echo.
    set /p continue="Devam etmek istiyor musunuz? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
    echo.
)

REM Virtual environment varsa aktiflestir
if exist "venv\Scripts\activate.bat" (
    echo [BILGI] Virtual environment aktiflestiriliyor...
    call venv\Scripts\activate.bat
)

REM videos dizini yoksa olustur
if not exist "videos" mkdir videos
if not exist "videos\temp_docs" mkdir videos\temp_docs

REM Ana programi calistir
echo [BILGI] Program baslatiliyor...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [HATA] Program hata verdi.
    pause
    exit /b 1
)
