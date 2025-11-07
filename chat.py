"""
Chat Arayüzü
Gemini ile interaktif sohbet için gelişmiş arayüz
"""

import os
import sys
from gemini_client import GeminiClient


class ChatInterface:
    def __init__(self):
        """Chat arayüzünü başlat"""
        self.client = GeminiClient()
        self.videos_loaded = False

    def display_banner(self):
        """Başlangıç banner'ını göster"""
        print("\n" + "="*70)
        print(" " * 20 + "📺 YouTube Kanal Analiz Aracı")
        print("="*70)

    def load_videos(self, videos_dir="videos"):
        """Video dosyalarını yükle"""
        print("\n📂 Video dosyaları yükleniyor...\n")

        # Videoları Gemini'ye yükle
        uploaded_files = self.client.upload_videos_to_gemini(videos_dir)

        if uploaded_files:
            self.videos_loaded = True
            return True
        else:
            print("\n❌ Video dosyası yüklenemedi!")
            return False

    def start_chat(self):
        """Chat oturumunu başlat"""
        if not self.videos_loaded:
            print("\n⚠️ Önce video dosyalarını yüklemelisiniz!")
            return

        # Chat başlat
        context = """
Kullanıcı kanal videolarıyla ilgili sorular soracak.
Örnek sorular:
- "En çok izlenen videolar hangileri?"
- "Son videolarda hangi konular işlendi?"
- "X konusu hakkında hangi videolar var?"
"""
        self.client.initialize_chat(context)

        # Chat döngüsü
        self.chat_loop()

    def chat_loop(self):
        """İnteraktif chat döngüsü"""
        print("\n" + "="*70)
        print("💬 Chat Başladı!")
        print("="*70)
        print("\nKomutlar:")
        print("  - 'çıkış' veya 'q': Çıkış yap")
        print("  - 'yardım' veya 'h': Örnek sorular göster")
        print("  - 'temizle' veya 'c': Ekranı temizle")
        print("\n" + "-"*70 + "\n")

        while True:
            # Kullanıcı mesajı al
            try:
                user_message = input("🙋 Siz: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Görüşürüz!")
                break

            if not user_message:
                continue

            # Komutları kontrol et
            if user_message.lower() in ['çıkış', 'exit', 'quit', 'q']:
                print("\n👋 Görüşürüz!")
                break

            elif user_message.lower() in ['yardım', 'help', 'h']:
                self.show_help()
                continue

            elif user_message.lower() in ['temizle', 'clear', 'c']:
                os.system('clear' if os.name != 'nt' else 'cls')
                print("\n" + "="*70)
                print("💬 Chat Devam Ediyor...")
                print("="*70 + "\n")
                continue

            # Mesaj gönder
            print("\n🤖 Gemini: ", end="", flush=True)
            response = self.client.send_message(user_message)

            if response:
                print(response)
            else:
                print("Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.")

            print("\n" + "-"*70 + "\n")

    def show_help(self):
        """Yardım mesajı göster"""
        print("\n" + "="*70)
        print("📖 Örnek Sorular")
        print("="*70)
        print("""
1. Genel Sorular:
   - "Kaç video var?"
   - "En popüler videolar hangileri?"
   - "En son yayınlanan videolar hangileri?"

2. İçerik Sorguları:
   - "Python hakkında hangi videolar var?"
   - "Yapay zeka konusunda ne anlatılmış?"
   - "En çok izlenen video hangisi ve ne anlatıyor?"

3. Analiz Soruları:
   - "Hangi konular en çok işlenmiş?"
   - "Videolardaki ana temalar neler?"
   - "Son 5 videoda hangi konular var?"

4. Özel Aramalar:
   - "X tarihinden sonra yayınlanan videolar"
   - "Y kelimesi geçen videolar"
   - "Z süreden uzun videolar"
""")
        print("="*70 + "\n")

    def run(self):
        """Ana program akışı"""
        self.display_banner()

        # Video dizinini kontrol et
        videos_dir = "videos"

        if not os.path.exists(videos_dir):
            print(f"\n⚠️ '{videos_dir}' dizini bulunamadı!")
            print("Lütfen önce 'main.py' ile videoları çekin.\n")
            return

        # JSON dosyalarını kontrol et
        json_files = [f for f in os.listdir(videos_dir) if f.endswith('.json')]

        if not json_files:
            print(f"\n⚠️ '{videos_dir}' dizininde video dosyası bulunamadı!")
            print("Lütfen önce 'main.py' ile videoları çekin.\n")
            return

        print(f"\n✅ {len(json_files)} video dosyası bulundu")

        # Videoları yükle
        if self.load_videos(videos_dir):
            # Chat başlat
            self.start_chat()


if __name__ == "__main__":
    chat = ChatInterface()
    chat.run()
