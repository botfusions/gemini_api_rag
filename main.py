"""
YouTube Kanal Analiz Aracı - Ana Script
Tüm işlemleri tek yerden yönetir
"""

import os
import sys
from youtube_scraper import YouTubeScraper
from translator import Translator
from gemini_client import GeminiClient


def print_banner():
    """Başlık banner'ını göster"""
    print("\n" + "="*80)
    print(" " * 25 + "📺 YouTube Kanal Analiz Aracı")
    print("="*80)


def print_menu():
    """Ana menüyü göster"""
    print("\n" + "-"*80)
    print("ANA MENÜ")
    print("-"*80)
    print("1. Yeni kanal analiz et")
    print("2. Mevcut videoları Türkçe'ye çevir")
    print("3. Videoları Gemini'ye yükle")
    print("4. Chat'i başlat")
    print("5. Tüm işlemleri sırayla yap (1-2-3-4)")
    print("0. Çıkış")
    print("-"*80)


def scrape_channel():
    """YouTube kanalından videoları çek"""
    print("\n" + "="*80)
    print("1️⃣ KANAL VİDEOLARINI ÇEK")
    print("="*80)

    # Kanal URL'si al
    channel_url = input("\n📝 YouTube kanal URL'sini girin: ").strip()

    if not channel_url:
        print("❌ Geçersiz URL!")
        return False

    # Video sayısı al
    try:
        max_videos = int(input("📝 Kaç video çekilsin? (varsayılan: 50): ").strip() or "50")
    except ValueError:
        print("⚠️ Geçersiz sayı, varsayılan olarak 50 video çekilecek")
        max_videos = 50

    # Scraper oluştur
    scraper = YouTubeScraper()

    # Videoları çek
    videos = scraper.fetch_channel_videos(channel_url, max_videos)

    if not videos:
        print("\n❌ Video bulunamadı!")
        return False

    # Her video için altyazı çek ve kaydet
    print("\n" + "="*80)
    print(f"📥 {len(videos)} video için altyazılar çekiliyor...")
    print("="*80)

    success_count = 0
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] İşleniyor: {video.get('title', 'İsimsiz')[:60]}...")
        video_url = video.get('url', '')

        if video_url:
            transcript = scraper.fetch_video_transcript(video_url)
            filepath = scraper.save_video_data(video, transcript)

            if filepath:
                success_count += 1

    print(f"\n✨ {success_count}/{len(videos)} video başarıyla kaydedildi!")
    return success_count > 0


def translate_videos():
    """Video altyazılarını Türkçe'ye çevir"""
    print("\n" + "="*80)
    print("2️⃣ ALTYAZILARI TÜRKÇE'YE ÇEVİR")
    print("="*80)

    # Çevirici oluştur
    translator = Translator()

    # Tüm videoları çevir
    success_count = translator.translate_all_videos()

    return success_count > 0


def upload_to_gemini():
    """Videoları Gemini'ye yükle"""
    print("\n" + "="*80)
    print("3️⃣ VİDEOLARI GEMİNİ'YE YÜKLE")
    print("="*80)

    # Gemini client oluştur
    client = GeminiClient()

    # Videoları yükle
    uploaded_files = client.upload_videos_to_gemini()

    return len(uploaded_files) > 0


def start_chat():
    """Chat arayüzünü başlat"""
    print("\n" + "="*80)
    print("4️⃣ CHAT'İ BAŞLAT")
    print("="*80)

    # Chat modülünü çalıştır
    from chat import ChatInterface

    chat = ChatInterface()

    # Videoları yükle
    if not chat.load_videos():
        return False

    # Chat başlat
    chat.start_chat()

    return True


def run_all():
    """Tüm işlemleri sırayla yap"""
    print("\n" + "="*80)
    print("🚀 TÜM İŞLEMLER BAŞLIYOR")
    print("="*80)

    # 1. Kanal videolarını çek
    if not scrape_channel():
        print("\n❌ Video çekme başarısız!")
        return False

    input("\n⏸️  Devam etmek için Enter'a basın...")

    # 2. Altyazıları çevir
    if not translate_videos():
        print("\n❌ Çeviri başarısız!")
        return False

    input("\n⏸️  Devam etmek için Enter'a basın...")

    # 3. Gemini'ye yükle
    if not upload_to_gemini():
        print("\n❌ Gemini'ye yükleme başarısız!")
        return False

    input("\n⏸️  Devam etmek için Enter'a basın...")

    # 4. Chat başlat
    start_chat()

    return True


def main():
    """Ana program"""
    print_banner()

    while True:
        print_menu()

        try:
            choice = input("\nSeçiminiz: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Görüşürüz!")
            break

        if choice == '0':
            print("\n👋 Görüşürüz!")
            break

        elif choice == '1':
            scrape_channel()

        elif choice == '2':
            translate_videos()

        elif choice == '3':
            upload_to_gemini()

        elif choice == '4':
            start_chat()

        elif choice == '5':
            run_all()

        else:
            print("\n❌ Geçersiz seçim!")

        input("\n⏸️  Ana menüye dönmek için Enter'a basın...")


if __name__ == "__main__":
    main()
