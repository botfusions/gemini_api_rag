#!/bin/bash

# YouTube Kanal Analiz Aracı - Kurulum Scripti

echo "🚀 YouTube Kanal Analiz Aracı Kurulumu Başlıyor..."
echo ""

# Python versiyonu kontrolü
echo "📌 Python versiyonu kontrol ediliyor..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 bulunamadı. Lütfen Python 3.8+ yükleyin."
    exit 1
fi
echo "✅ Python bulundu"
echo ""

# Virtual environment oluştur (isteğe bağlı)
read -p "🤔 Virtual environment oluşturmak ister misiniz? (y/n): " use_venv
if [ "$use_venv" = "y" ] || [ "$use_venv" = "Y" ]; then
    echo "📦 Virtual environment oluşturuluyor..."
    python3 -m venv venv

    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "✅ Virtual environment aktif"
    else
        echo "⚠️ Virtual environment oluşturulamadı, devam ediliyor..."
    fi
    echo ""
fi

# Bağımlılıkları yükle
echo "📦 Bağımlılıklar yükleniyor..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Bağımlılıklar yüklenemedi."
    exit 1
fi
echo "✅ Bağımlılıklar yüklendi"
echo ""

# .env dosyası oluştur
if [ ! -f ".env" ]; then
    echo "🔑 .env dosyası oluşturuluyor..."
    cp .env.example .env
    echo "✅ .env dosyası oluşturuldu"
    echo ""
    echo "⚠️  ÖNEMLİ: .env dosyasını düzenleyip API anahtarlarınızı ekleyin!"
    echo ""
    echo "API Anahtarları için:"
    echo "  - Apify: https://console.apify.com/account/integrations"
    echo "  - Gemini: https://makersuite.google.com/app/apikey"
    echo ""
else
    echo "✅ .env dosyası zaten mevcut"
    echo ""
fi

# videos dizini oluştur
if [ ! -d "videos" ]; then
    mkdir -p videos/temp_docs
    echo "✅ videos dizini oluşturuldu"
else
    echo "✅ videos dizini mevcut"
fi
echo ""

# Kurulum tamamlandı
echo "🎉 Kurulum tamamlandı!"
echo ""
echo "Sıradaki adımlar:"
echo "1. .env dosyasını düzenleyin ve API anahtarlarınızı ekleyin"
if [ "$use_venv" = "y" ] || [ "$use_venv" = "Y" ]; then
    echo "2. Virtual environment'ı aktifleştirin: source venv/bin/activate"
    echo "3. Programı çalıştırın: python main.py"
else
    echo "2. Programı çalıştırın: python main.py"
fi
echo ""
echo "Veya hızlı başlatma için: ./run.sh"
echo ""
