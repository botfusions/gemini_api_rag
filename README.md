# 📺 YouTube Kanal Analiz Aracı

YouTube kanallarındaki videoları analiz eden, altyazıları Türkçe'ye çeviren ve Gemini AI ile sohbet etmenizi sağlayan kapsamlı bir araç.

## 🌟 Özellikler

- ✅ YouTube kanallarından video bilgilerini çekme
- ✅ Video altyazılarını otomatik çekme
- ✅ Altyazıları Türkçe'ye çevirme
- ✅ Videoları Gemini AI'a yükleme
- ✅ Videolar hakkında Türkçe sohbet arayüzü
- ✅ Modüler ve genişletilebilir yapı

## 📋 Gereksinimler

- Python 3.8+
- Apify API anahtarı
- Google Gemini API anahtarı

## 🚀 Kurulum

1. **Repoyu klonlayın:**
```bash
git clone <repo-url>
cd gemini_api_rag
```

2. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

3. **API anahtarlarını ayarlayın:**

`.env.example` dosyasını `.env` olarak kopyalayın:
```bash
cp .env.example .env
```

`.env` dosyasını düzenleyip API anahtarlarınızı ekleyin:
```
APIFY_API_KEY=your_apify_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## 💡 Kullanım

### Yöntem 1: Ana Script (Önerilen)

Interaktif menü ile tüm işlemleri yönetin:

```bash
python main.py
```

Ana menü seçenekleri:
1. **Yeni kanal analiz et** - YouTube kanalından videoları çeker
2. **Mevcut videoları Türkçe'ye çevir** - Çekilen altyazıları çevirir
3. **Videoları Gemini'ye yükle** - Çevrilmiş videoları AI'a yükler
4. **Chat'i başlat** - Video içerikleri hakkında sohbet edin
5. **Tüm işlemleri sırayla yap** - 1-4 adımlarını otomatik yapar

### Yöntem 2: Modüler Kullanım

#### 1️⃣ Video Çekme

```bash
python youtube_scraper.py
```

Kanal URL'si girin ve videolar `videos/` dizinine kaydedilir.

#### 2️⃣ Çeviri

```bash
python translator.py
```

`videos/` dizinindeki tüm videoların altyazıları Türkçe'ye çevrilir.

#### 3️⃣ Gemini'ye Yükleme ve Chat

```bash
python chat.py
```

Videoları Gemini'ye yükler ve sohbet arayüzünü başlatır.

## 📁 Proje Yapısı

```
gemini_api_rag/
├── main.py              # Ana program
├── youtube_scraper.py   # YouTube video çekme modülü
├── translator.py        # Çeviri modülü
├── gemini_client.py     # Gemini API istemcisi
├── chat.py              # Chat arayüzü
├── requirements.txt     # Python bağımlılıkları
├── .env.example         # Örnek çevre değişkenleri
├── .env                 # API anahtarları (gitignore'da)
├── README.md            # Bu dosya
└── videos/              # Video verilerinin saklandığı dizin
    ├── {video_id}.json  # Her video için JSON dosyası
    └── temp_docs/       # Gemini için geçici metin dosyaları
```

## 📝 Video Veri Formatı

Her video için oluşturulan JSON dosyası şu bilgileri içerir:

```json
{
  "id": "video_id",
  "title": "Video Başlığı",
  "description": "Video açıklaması",
  "publishedAt": "2024-01-01",
  "url": "https://youtube.com/watch?v=...",
  "thumbnail": "thumbnail_url",
  "views": 1000,
  "likes": 50,
  "duration": "PT10M30S",
  "transcript": "Orijinal altyazı...",
  "transcript_tr": "Türkçe çeviri..."
}
```

## 💬 Chat Özellikleri

Chat arayüzü ile yapabilecekleriniz:

### Genel Sorular
- "Kaç video var?"
- "En popüler videolar hangileri?"
- "En son yayınlanan videolar hangileri?"

### İçerik Sorguları
- "Python hakkında hangi videolar var?"
- "Yapay zeka konusunda ne anlatılmış?"
- "En çok izlenen video hangisi ve ne anlatıyor?"

### Analiz Soruları
- "Hangi konular en çok işlenmiş?"
- "Videolardaki ana temalar neler?"
- "Son 5 videoda hangi konular var?"

### Chat Komutları
- `çıkış` veya `q` - Chat'ten çık
- `yardım` veya `h` - Örnek sorular göster
- `temizle` veya `c` - Ekranı temizle

## 🔧 API Anahtarları Nasıl Alınır?

### Apify API Anahtarı

1. [Apify](https://apify.com/) sitesine üye olun
2. Hesap ayarlarından API anahtarınızı kopyalayın
3. `.env` dosyasına `APIFY_API_KEY` olarak ekleyin

### Gemini API Anahtarı

1. [Google AI Studio](https://makersuite.google.com/app/apikey) sayfasına gidin
2. "Create API Key" butonuna tıklayın
3. Anahtarı kopyalayın ve `.env` dosyasına `GEMINI_API_KEY` olarak ekleyin

## ⚙️ Yapılandırma

### Video Sayısı Ayarlama

`youtube_scraper.py` veya `main.py` içinde `max_videos` parametresini değiştirin:

```python
videos = scraper.fetch_channel_videos(channel_url, max_videos=100)
```

### Çeviri Dili Değiştirme

`translator.py` içinde hedef dili değiştirin:

```python
self.translator = GoogleTranslator(source='auto', target='en')  # İngilizce için
```

## 🐛 Sorun Giderme

### "APIFY_API_KEY bulunamadı" hatası
- `.env` dosyasının proje kök dizininde olduğundan emin olun
- API anahtarının doğru formatta olduğunu kontrol edin

### "Video bulunamadı" hatası
- Kanal URL'sinin doğru olduğundan emin olun
- Kanalın herkese açık olduğunu kontrol edin
- Apify limitlerini kontrol edin

### Çeviri çok yavaş
- `translator.py` içindeki `time.sleep()` değerini artırın (rate limiting)
- Daha az video ile test edin

### Gemini yükleme hatası
- API anahtarının geçerli olduğundan emin olun
- Gemini API limitlerini kontrol edin
- İnternet bağlantınızı kontrol edin

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Teşekkürler

- [Apify](https://apify.com/) - YouTube scraping için
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI chat için
- [deep-translator](https://github.com/nidhaloff/deep-translator) - Çeviri için

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not:** Bu araç eğitim amaçlıdır. YouTube'un kullanım şartlarına uygun kullanın.
