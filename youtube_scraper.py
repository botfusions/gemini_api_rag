"""
YouTube Kanal Video Çekme Modülü
Apify kullanarak YouTube kanallarından video bilgilerini çeker
"""

import os
from apify_client import ApifyClient
from dotenv import load_dotenv
import json
from datetime import datetime
import re

# YouTube Transcript API import
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    print("⚠️ youtube-transcript-api yüklü değil. Sadece Apify kullanılacak.")
    TRANSCRIPT_API_AVAILABLE = False

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

    def extract_video_id(self, video_url):
        """
        YouTube video URL'sinden video ID'sini çıkar

        Args:
            video_url (str): YouTube video URL'si

        Returns:
            str: Video ID veya None
        """
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, video_url)
            if match:
                return match.group(1)
        return None

    def fetch_transcript_with_api(self, video_url):
        """
        youtube-transcript-api kullanarak altyazı çek

        Args:
            video_url (str): YouTube video URL'si

        Returns:
            str: Video altyazı metni
        """
        if not TRANSCRIPT_API_AVAILABLE:
            print("⚠️ youtube-transcript-api mevcut değil")
            return ""

        try:
            video_id = self.extract_video_id(video_url)
            if not video_id:
                print(f"⚠️ Video ID çıkarılamadı: {video_url}")
                return ""

            print(f"   Video ID: {video_id}")

            # Önce Türkçe altyazı dene
            try:
                print("   Türkçe altyazı deneniyor...")
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['tr'])
                print(f"   ✅ Türkçe altyazı bulundu!")
            except Exception as e1:
                print(f"   ⚠️ Türkçe altyazı yok: {str(e1)[:50]}")
                # Türkçe yoksa İngilizce dene
                try:
                    print("   İngilizce altyazı deneniyor...")
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    print(f"   ✅ İngilizce altyazı bulundu!")
                except Exception as e2:
                    print(f"   ⚠️ İngilizce altyazı yok: {str(e2)[:50]}")
                    # Otomatik oluşturulan altyazıları al
                    print("   Otomatik oluşturulan altyazılar deneniyor...")
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    print(f"   ✅ Otomatik altyazı bulundu!")

            # Altyazıları birleştir
            transcript = ' '.join([item['text'] for item in transcript_list])
            print(f"✅ YouTube Transcript API ile altyazı bulundu ({len(transcript)} karakter)")
            return transcript

        except Exception as e:
            print(f"❌ YouTube Transcript API HATASI:")
            print(f"   Hata tipi: {type(e).__name__}")
            print(f"   Hata mesajı: {str(e)}")
            import traceback
            print(f"   Detay: {traceback.format_exc()[:500]}")
            return ""

    def fetch_video_transcript(self, video_url):
        """
        Verilen video URL'sinden altyazıları çek
        Önce Apify kullanır, başarısız olursa youtube-transcript-api ile dener

        Args:
            video_url (str): YouTube video URL'si

        Returns:
            str: Video altyazı metni
        """
        print(f"📝 Altyazı çekiliyor: {video_url}")

        # Önce Apify ile dene
        run_input = {
            "startUrls": [{"url": video_url}],
            "subtitlesLanguage": "en",  # Altyazı dilini belirt
            "subtitlesFormat": "text",  # Text formatında al
        }

        try:
            # Actor'ü çalıştır
            run = self.client.actor("streamers/youtube-scraper").call(run_input=run_input)

            # Sonuçları al
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                # Altyazı varsa döndür
                if 'subtitles' in item and item['subtitles']:
                    transcript = ' '.join([sub.get('text', '') for sub in item['subtitles']])
                    print(f"✅ Apify ile altyazı bulundu ({len(transcript)} karakter)")
                    return transcript

        except Exception as e:
            print(f"⚠️ Apify hatası: {str(e)}")

        # Apify başarısız olduysa youtube-transcript-api ile dene
        print("🔄 YouTube Transcript API deneniyor...")
        transcript = self.fetch_transcript_with_api(video_url)

        if transcript:
            return transcript

        # Hiçbir yöntem işe yaramadıysa boş döndür
        print("⚠️ Altyazı bulunamadı")
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
