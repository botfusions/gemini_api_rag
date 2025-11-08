"""
Gemini API İstemcisi
Video dosyalarını Gemini'ye yükler ve chat arayüzü sağlar
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import time

# .env dosyasından çevre değişkenlerini yükle
load_dotenv()


class GeminiClient:
    def __init__(self):
        """Gemini API client'ı başlat"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.uploaded_files = []
        self.chat = None

    def create_video_document(self, video_filepath):
        """
        Video JSON dosyasından metin dökümanı oluştur

        Args:
            video_filepath (str): Video JSON dosya yolu

        Returns:
            str: Döküman metni
        """
        try:
            with open(video_filepath, 'r', encoding='utf-8') as f:
                video_data = json.load(f)

            # Döküman oluştur
            doc = f"""
# {video_data.get('title', 'İsimsiz Video')}

**Video ID:** {video_data.get('id', '')}
**Yayın Tarihi:** {video_data.get('publishedAt', '')}
**URL:** {video_data.get('url', '')}
**Görüntülenme:** {video_data.get('views', 0)}
**Beğeni:** {video_data.get('likes', 0)}
**Süre:** {video_data.get('duration', '')}

## Açıklama
{video_data.get('description', '')}

## Altyazı (Türkçe)
{video_data.get('transcript_tr', video_data.get('transcript', ''))}
"""
            return doc

        except Exception as e:
            print(f"❌ Döküman oluşturma hatası: {str(e)}")
            return ""

    def upload_videos_to_gemini(self, videos_dir="videos"):
        """
        Tüm video dosyalarını Gemini'ye yükle

        Args:
            videos_dir (str): Video dosyalarının bulunduğu dizin

        Returns:
            list: Yüklenen dosya bilgileri
        """
        if not os.path.exists(videos_dir):
            print(f"❌ Dizin bulunamadı: {videos_dir}")
            return []

        # Tüm JSON dosyalarını bul
        json_files = [f for f in os.listdir(videos_dir) if f.endswith('.json')]

        if not json_files:
            print(f"⚠️ JSON dosyası bulunamadı: {videos_dir}")
            return []

        print(f"📚 {len(json_files)} dosya bulundu")

        # Geçici metin dosyaları için dizin oluştur
        temp_dir = os.path.join(videos_dir, "temp_docs")
        os.makedirs(temp_dir, exist_ok=True)

        uploaded_files = []

        # Her dosyayı işle
        for i, filename in enumerate(json_files, 1):
            filepath = os.path.join(videos_dir, filename)
            print(f"\n[{i}/{len(json_files)}] Yükleniyor: {filename}")

            try:
                # Metin dökümanı oluştur
                doc_content = self.create_video_document(filepath)

                if not doc_content:
                    print(f"⚠️ Döküman oluşturulamadı: {filename}")
                    continue

                # Geçici metin dosyası oluştur
                temp_filename = filename.replace('.json', '.txt')
                temp_filepath = os.path.join(temp_dir, temp_filename)

                with open(temp_filepath, 'w', encoding='utf-8') as f:
                    f.write(doc_content)

                # Gemini'ye yükle
                uploaded_file = genai.upload_file(temp_filepath)
                uploaded_files.append(uploaded_file)

                print(f"✅ Yüklendi: {uploaded_file.name}")

                # Rate limiting için bekle
                if i < len(json_files):
                    time.sleep(1)

            except Exception as e:
                print(f"❌ Yükleme hatası: {str(e)}")
                continue

        self.uploaded_files = uploaded_files
        print(f"\n✨ {len(uploaded_files)}/{len(json_files)} dosya başarıyla yüklendi")
        return uploaded_files

    def initialize_chat(self, context=""):
        """
        Chat oturumu başlat

        Args:
            context (str): Başlangıç bağlamı
        """
        if not self.uploaded_files:
            print("⚠️ Henüz dosya yüklenmedi!")
            return

        # Sistem talimatı
        system_instruction = f"""
Sen bir YouTube kanal analiz asistanısın. Kullanıcıya kanal videolarıyla ilgili sorularını cevapla.

{len(self.uploaded_files)} video dosyası yüklendi. Bu videolar hakkında detaylı bilgi verebilirsin.

{context}

Lütfen:
- Türkçe cevap ver
- Net ve anlaşılır ol
- Video başlıkları, tarihleri ve içeriklerine atıfta bulun
- Gerektiğinde video URL'lerini paylaş
"""

        # Chat başlat
        self.chat = self.model.start_chat(history=[])

        # İlk mesajı gönder (dosyalarla birlikte)
        initial_message = [system_instruction] + self.uploaded_files
        response = self.chat.send_message(initial_message)

        print("💬 Chat başlatıldı!")
        return response

    def send_message(self, message):
        """
        Chat'e mesaj gönder

        Args:
            message (str): Kullanıcı mesajı

        Returns:
            str: Gemini'nin cevabı
        """
        if not self.chat:
            print("⚠️ Chat başlatılmadı! Önce initialize_chat() çağırın.")
            return ""

        try:
            response = self.chat.send_message(message)
            return response.text

        except Exception as e:
            print(f"❌ Mesaj gönderme hatası: {str(e)}")
            return ""

    def chat_loop(self):
        """
        Interaktif chat döngüsü
        """
        if not self.chat:
            print("⚠️ Chat başlatılmadı!")
            return

        print("\n" + "="*60)
        print("💬 YouTube Kanal Analiz Chat'i")
        print("="*60)
        print("'çıkış' yazarak çıkabilirsiniz\n")

        while True:
            # Kullanıcı mesajı al
            user_message = input("Siz: ").strip()

            if not user_message:
                continue

            if user_message.lower() in ['çıkış', 'exit', 'quit', 'q']:
                print("\n👋 Görüşürüz!")
                break

            # Mesaj gönder
            print("\n🤖 Gemini: ", end="", flush=True)
            response = self.send_message(user_message)

            if response:
                print(response)
            else:
                print("Üzgünüm, bir hata oluştu.")

            print()


if __name__ == "__main__":
    # Test için
    client = GeminiClient()

    # Videoları yükle
    client.upload_videos_to_gemini()

    # Chat başlat
    if client.uploaded_files:
        client.initialize_chat()
        client.chat_loop()
    else:
        print("❌ Yüklenmiş dosya bulunamadı!")
