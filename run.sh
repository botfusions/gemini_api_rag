#!/bin/bash

# YouTube Kanal Analiz Aracı - Çalıştırma Scripti

echo "📺 YouTube Kanal Analiz Aracı"
echo ""

# .env kontrolü
if [ ! -f ".env" ]; then
    echo "❌ .env dosyası bulunamadı!"
    echo "Lütfen önce setup.sh scriptini çalıştırın:"
    echo "  bash setup.sh"
    exit 1
fi

# API anahtarlarının girilip girilmediğini kontrol et
if grep -q "your_apify_api_key_here" .env || grep -q "your_gemini_api_key_here" .env; then
    echo "⚠️  UYARI: API anahtarları girilmemiş!"
    echo ""
    echo ".env dosyasını düzenleyip gerçek API anahtarlarınızı ekleyin:"
    echo "  nano .env"
    echo ""
    read -p "Devam etmek istiyor musunuz? (y/n): " continue
    if [ "$continue" != "y" ] && [ "$continue" != "Y" ]; then
        exit 1
    fi
fi

# Virtual environment varsa aktifleştir
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    echo "🔄 Virtual environment aktifleştiriliyor..."
    source venv/bin/activate
fi

# videos dizini yoksa oluştur
if [ ! -d "videos" ]; then
    mkdir -p videos/temp_docs
    echo "✅ videos dizini oluşturuldu"
fi

# Ana programı çalıştır
echo "🚀 Program başlatılıyor..."
echo ""
python main.py
