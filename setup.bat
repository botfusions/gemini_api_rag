@echo off
REM YouTube Kanal Analiz Araci - Kurulum Scripti (Windows)

echo.
echo ================================
echo YouTube Kanal Analiz Araci
echo Kurulum Basliyor...
echo ================================
echo.

REM Python versiyonu kontrolu
echo [1/5] Python versiyonu kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi. Lutfen Python 3.8+ yukleyin.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [TAMAM] Python bulundu
echo.

REM Virtual environment olustur (istege bagli)
set /p use_venv="[2/5] Virtual environment olusturmak ister misiniz? (y/n): "
if /i "%use_venv%"=="y" (
    echo Virtual environment olusturuluyor...
    python -m venv venv
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        echo [TAMAM] Virtual environment aktif
    ) else (
        echo [UYARI] Virtual environment olusturulamadi, devam ediliyor...
    )
    echo.
)

REM Bagimliliklari yukle
echo [3/5] Bagimliluklar yukleniyor...
pip install -r requirements.txt
if errorlevel 1 (
    echo [HATA] Bagimliluklar yuklenemedi.
    pause
    exit /b 1
)
echo [TAMAM] Bagimliluklar yuklendi
echo.

REM .env dosyasi olustur
echo [4/5] .env dosyasi kontrol ediliyor...
if not exist ".env" (
    echo .env dosyasi olusturuluyor...
    copy .env.example .env >nul
    echo [TAMAM] .env dosyasi olusturuldu
    echo.
    echo =====================================
    echo   ONEMLI: API Anahtarlarini Ekleyin!
    echo =====================================
    echo.
    echo .env dosyasini duzenleyip API anahtarlarinizi ekleyin:
    echo   notepad .env
    echo.
    echo API Anahtarlari icin:
    echo   - Apify: https://console.apify.com/account/integrations
    echo   - Gemini: https://makersuite.google.com/app/apikey
    echo.
) else (
    echo [TAMAM] .env dosyasi zaten mevcut
    echo.
)

REM videos dizini olustur
echo [5/5] Klasorler olusturuluyor...
if not exist "videos" mkdir videos
if not exist "videos\temp_docs" mkdir videos\temp_docs
echo [TAMAM] Gerekli klasorler olusturuldu
echo.

echo ================================
echo   Kurulum Tamamlandi!
echo ================================
echo.
echo Siradaki adimlar:
echo 1. .env dosyasini duzenleyin: notepad .env
echo 2. API anahtarlarinizi ekleyin
if /i "%use_venv%"=="y" (
    echo 3. Virtual environment'i aktifestirin: venv\Scripts\activate
    echo 4. Programi calistirin: python main.py
) else (
    echo 3. Programi calistirin: python main.py
)
echo.
echo Veya hizli baslatma icin: run.bat
echo.
pause
