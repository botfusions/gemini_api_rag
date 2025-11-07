"""
YouTube Kanal Video Çekme Modülü
Apify kullanarak YouTube kanallarından video bilgilerini çeker
"""

import os
from apify_client import ApifyClient
from dotenv import load_dotenv
import json
from datetime import datetime

# .env dosyasından çevre değişkenlerini yükle
load_dotenv()


class YouTubeScraper:
    def __init__(self):
        """Apify client'ı başlat"""
        api_key = os.getenv('APIFY_API_KEY')
        if not api_key:
            raise ValueError("APIFY_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")

        self.client = ApifyClient(api_key)

    def fetch_channel_videos(self, channel_url, max_videos=50):
        """
        Verilen YouTube kanal URL'sinden videoları çek

        Args:
            channel_url (str): YouTube kanal URL'si
            max_videos (int): Çekilecek maksimum video sayısı

        Returns:
            list: Video bilgilerini içeren liste
        """
        print(f"📺 Kanal videoları çekiliyor: {channel_url}")

        # Apify YouTube Scraper actor'ünü kullan
        # Actor ID: streamers/youtube-scraper
        run_input = {
            "startUrls": [{"url": channel_url}],
            "maxResults": max_videos,
            "searchType": "channel",
        }

        try:
            # Actor'ü çalıştır
            run = self.client.actor("streamers/youtube-scraper").call(run_input=run_input)

            # Sonuçları al
            videos = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                videos.append(item)

            # Videoları tarih sırasına göre sırala (en yeni en başta)
            videos.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)

            print(f"✅ {len(videos)} video bulundu")
            return videos

        except Exception as e:
            print(f"❌ Hata oluştu: {str(e)}")
            return []

    def fetch_video_transcript(self, video_url):
        """
        Verilen video URL'sinden altyazıları çek

        Args:
            video_url (str): YouTube video URL'si

        Returns:
            str: Video altyazı metni
        """
        print(f"📝 Altyazı çekiliyor: {video_url}")

        # Apify YouTube Transcript Scraper actor'ünü kullan
        run_input = {
            "startUrls": [{"url": video_url}],
        }

        try:
            # Actor'ü çalıştır
            run = self.client.actor("streamers/youtube-scraper").call(run_input=run_input)

            # Sonuçları al
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                # Altyazı varsa döndür
                if 'subtitles' in item and item['subtitles']:
                    transcript = ' '.join([sub.get('text', '') for sub in item['subtitles']])
                    print(f"✅ Altyazı bulundu ({len(transcript)} karakter)")
                    return transcript
                elif 'description' in item:
                    print("⚠️ Altyazı bulunamadı, açıklama kullanılıyor")
                    return item['description']

            print("⚠️ Altyazı bulunamadı")
            return ""

        except Exception as e:
            print(f"❌ Altyazı çekilirken hata: {str(e)}")
            return ""

    def save_video_data(self, video, transcript, output_dir="videos"):
        """
        Video bilgilerini ve altyazısını dosyaya kaydet

        Args:
            video (dict): Video bilgileri
            transcript (str): Video altyazısı
            output_dir (str): Çıktı dizini

        Returns:
            str: Oluşturulan dosya yolu
        """
        # Çıktı dizinini oluştur
        os.makedirs(output_dir, exist_ok=True)

        # Dosya adı oluştur (video ID kullan)
        video_id = video.get('id', 'unknown')
        filename = f"{video_id}.json"
        filepath = os.path.join(output_dir, filename)

        # Video verisini hazırla
        video_data = {
            'id': video.get('id', ''),
            'title': video.get('title', ''),
            'description': video.get('description', ''),
            'publishedAt': video.get('publishedAt', ''),
            'url': video.get('url', ''),
            'thumbnail': video.get('thumbnail', ''),
            'views': video.get('viewCount', 0),
            'likes': video.get('likeCount', 0),
            'duration': video.get('duration', ''),
            'transcript': transcript,
            'transcript_tr': '',  # Çeviri için boş bırak
        }

        # Dosyaya kaydet
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(video_data, f, ensure_ascii=False, indent=2)

        print(f"💾 Kaydedildi: {filepath}")
        return filepath


if __name__ == "__main__":
    # Test için
    scraper = YouTubeScraper()

    # Örnek kanal URL'si
    channel_url = input("YouTube kanal URL'sini girin: ")

    # Videoları çek
    videos = scraper.fetch_channel_videos(channel_url, max_videos=10)

    # Her video için altyazı çek ve kaydet
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] İşleniyor: {video.get('title', 'İsimsiz')}")
        video_url = video.get('url', '')

        if video_url:
            transcript = scraper.fetch_video_transcript(video_url)
            scraper.save_video_data(video, transcript)

    print("\n✨ Tüm videolar işlendi!")
