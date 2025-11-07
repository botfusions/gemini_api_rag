"""
Çeviri Modülü
Video altyazılarını Türkçe'ye çevirir
"""

import os
import json
from deep_translator import GoogleTranslator
import time


class Translator:
    def __init__(self):
        """Çevirici başlat"""
        self.translator = GoogleTranslator(source='auto', target='tr')

    def translate_text(self, text, chunk_size=5000):
        """
        Metni Türkçe'ye çevir

        Args:
            text (str): Çevrilecek metin
            chunk_size (int): Her seferinde çevrilecek maksimum karakter sayısı

        Returns:
            str: Çevrilmiş metin
        """
        if not text or len(text.strip()) == 0:
            return ""

        try:
            # Uzun metinleri parçalara böl
            if len(text) <= chunk_size:
                translated = self.translator.translate(text)
                return translated
            else:
                # Metni parçalara böl
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                translated_chunks = []

                print(f"📄 Metin {len(chunks)} parçaya bölündü")

                for i, chunk in enumerate(chunks, 1):
                    print(f"   Çevriliyor: {i}/{len(chunks)}")
                    translated = self.translator.translate(chunk)
                    translated_chunks.append(translated)

                    # Rate limiting için bekle
                    if i < len(chunks):
                        time.sleep(1)

                return ' '.join(translated_chunks)

        except Exception as e:
            print(f"❌ Çeviri hatası: {str(e)}")
            return text  # Hata durumunda orijinal metni döndür

    def translate_video_file(self, filepath):
        """
        Video JSON dosyasındaki altyazıyı çevir

        Args:
            filepath (str): Video JSON dosya yolu

        Returns:
            bool: Başarılı ise True
        """
        try:
            # Dosyayı oku
            with open(filepath, 'r', encoding='utf-8') as f:
                video_data = json.load(f)

            # Altyazı varsa çevir
            transcript = video_data.get('transcript', '')
            if transcript and len(transcript.strip()) > 0:
                print(f"🔄 Çevriliyor: {video_data.get('title', 'İsimsiz')}")

                # Çevir
                translated = self.translate_text(transcript)
                video_data['transcript_tr'] = translated

                # Dosyayı güncelle
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(video_data, f, ensure_ascii=False, indent=2)

                print(f"✅ Çeviri tamamlandı")
                return True
            else:
                print(f"⚠️ Altyazı bulunamadı: {filepath}")
                return False

        except Exception as e:
            print(f"❌ Dosya işleme hatası: {str(e)}")
            return False

    def translate_all_videos(self, videos_dir="videos"):
        """
        Tüm video dosyalarındaki altyazıları çevir

        Args:
            videos_dir (str): Video dosyalarının bulunduğu dizin

        Returns:
            int: Çevrilen dosya sayısı
        """
        if not os.path.exists(videos_dir):
            print(f"❌ Dizin bulunamadı: {videos_dir}")
            return 0

        # Tüm JSON dosyalarını bul
        json_files = [f for f in os.listdir(videos_dir) if f.endswith('.json')]

        if not json_files:
            print(f"⚠️ JSON dosyası bulunamadı: {videos_dir}")
            return 0

        print(f"📚 {len(json_files)} dosya bulundu")

        # Her dosyayı çevir
        success_count = 0
        for i, filename in enumerate(json_files, 1):
            filepath = os.path.join(videos_dir, filename)
            print(f"\n[{i}/{len(json_files)}] İşleniyor: {filename}")

            if self.translate_video_file(filepath):
                success_count += 1

            # Rate limiting için bekle
            if i < len(json_files):
                time.sleep(2)

        print(f"\n✨ {success_count}/{len(json_files)} dosya başarıyla çevrildi")
        return success_count


if __name__ == "__main__":
    # Test için
    translator = Translator()

    # Tüm videoları çevir
    translator.translate_all_videos()
