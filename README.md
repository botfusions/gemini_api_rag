# 📺 YouTube Kanal Analiz Aracı

YouTube kanallarındaki videoları analiz eden ve Gemini 2.5 Flash AI ile **Türkçe sohbet** etmenizi sağlayan kapsamlı bir araç.

## 🚀 Hızlı Başlangıç

```bash
# 1. Kurulum
git clone https://github.com/botfusions/gemini_api_rag.git
cd gemini_api_rag
pip install -r requirements.txt

# 2. API anahtarlarını ekle (.env dosyası)
cp .env.example .env
# APIFY_API_KEY ve GEMINI_API_KEY'i ekleyin

# 3. Çalıştır
python main.py
# Menüden "5. Tüm işlemleri sırayla yap" seçin
```

**Özellik:** Altyazılar İngilizce, ama Gemini 2.5 Flash **Türkçe cevap verir!** ✨

## 🌟 Özellikler

- ✅ YouTube kanallarından video bilgilerini çekme (Apify)
- ✅ Video altyazılarını otomatik çekme ve SRT parse etme
- ✅ Dual-source altyazı sistemi (Apify + youtube-transcript-api fallback)
- ✅ Videoları Gemini 2.5 Flash AI'a yükleme
- ✅ **Videolar hakkında Türkçe sohbet** (altyazılar İngilizce, cevaplar Türkçe)
- ✅ Modüler ve genişletilebilir yapı
- ✅ Hızlı ve ucuz (Gemini 2.5 Flash kullanıyor)

## 📋 Gereksinimler

- Python 3.8+
- Apify API anahtarı
- Google Gemini API anahtarı

## 🚀 Kurulum

### Linux / macOS

1. **Repoyu klonlayın:**
```bash
git clone https://github.com/botfusions/gemini_api_rag.git
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

### 🪟 Windows PowerShell

1. **Repoyu klonlayın:**
```powershell
git clone https://github.com/botfusions/gemini_api_rag.git
cd gemini_api_rag
```

2. **Sanal ortam oluşturun (önerilen):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Not:** Eğer çalıştırma izni hatası alırsanız:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **Bağımlılıkları yükleyin:**
```powershell
pip install -r requirements.txt
```

4. **API anahtarlarını ayarlayın:**
```powershell
# .env dosyasını oluştur
Copy-Item .env.example .env

# Not Defteri ile düzenle
notepad .env
```

`.env` dosyasına API anahtarlarınızı ekleyin:
```
APIFY_API_KEY=buraya_apify_anahtarinizi_yapisirin
GEMINI_API_KEY=buraya_gemini_anahtarinizi_yapisirin
```

5. **Programı çalıştırın:**
```powershell
python main.py
```

## 💡 Kullanım

### Yöntem 1: Ana Script (Önerilen)

Interaktif menü ile tüm işlemleri yönetin:

```bash
python main.py
```

Ana menü seçenekleri:
1. **Yeni kanal analiz et** - YouTube kanalından videoları çeker (İngilizce altyazılar)
2. **Mevcut videoları Türkçe'ye çevir** - ⚠️ ARTIK GEREKSIZ (Gemini 2.5 Flash direkt Türkçe konuşuyor)
3. **Videoları Gemini'ye yükle** - Videoları Gemini 2.5 Flash AI'a yükler
4. **Chat'i başlat** - Video içerikleri hakkında **Türkçe** sohbet edin
5. **Tüm işlemleri sırayla yap** - Hızlı başlangıç için tüm adımları otomatik yapar

### Yöntem 2: Modüler Kullanım

#### 1️⃣ Video Çekme

```bash
python youtube_scraper.py
```

Kanal URL'si girin ve videolar `videos/` dizinine kaydedilir (İngilizce altyazılarla).

#### 2️⃣ Çeviri (İsteğe Bağlı - Artık Gereksiz)

```bash
python translator.py
```

⚠️ **Not:** Gemini 2.5 Flash zaten İngilizce altyazıları okuyup Türkçe cevap veriyor. Bu adım artık gereksiz.

#### 3️⃣ Gemini'ye Yükleme ve Chat

```bash
python chat.py
```

Videoları Gemini 2.5 Flash'a yükler ve Türkçe sohbet arayüzünü başlatır.

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
  "transcript": "İngilizce altyazı metni (SRT'den parse edilmiş)"
}
```

⚠️ **Not:** `transcript_tr` alanı artık kullanılmıyor. Gemini 2.5 Flash direkt İngilizce altyazıları okuyup Türkçe cevap veriyor.

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

### Gemini Model Değiştirme

`gemini_client.py` içinde farklı Gemini modeli kullanabilirsiniz:

```python
self.model = genai.GenerativeModel('gemini-2.5-flash')  # Varsayılan (hızlı ve ucuz)
# veya
self.model = genai.GenerativeModel('gemini-1.5-pro')    # Daha güçlü ama pahalı
```

### Altyazı Dili Değiştirme

`youtube_scraper.py` içinde altyazı dilini değiştirebilirsiniz:

```python
run_input = {
    "subtitleLang": "tr",  # Türkçe altyazı için
    # veya "en", "es", "fr", vb.
}
```

## 🐛 Sorun Giderme

### "APIFY_API_KEY bulunamadı" hatası
- `.env` dosyasının proje kök dizininde olduğundan emin olun
- API anahtarının doğru formatta olduğunu kontrol edin

### "Video bulunamadı" hatası
- Kanal URL'sinin doğru olduğundan emin olun
- Kanalın herkese açık olduğunu kontrol edin
- Apify limitlerini kontrol edin

### Altyazı çekme sorunları

#### ✅ ÇÖZÜLDÜ: Apify Altyazı Parametreleri

**Sorun:** Apify `subtitles: None` döndürüyordu

**Çözüm:** Apify YouTube Scraper için doğru parametreler:
```python
run_input = {
    "startUrls": [{"url": video_url}],
    "downloadSubtitles": True,       # ✅ Doğru parametre
    "saveSubtitlesToKVS": True,      # ✅ Key-Value Store'a kaydet
    "subtitleLang": "en",            # ✅ Dil (tr, en, vb.)
    "preferAutoGeneratedSubtitles": False,  # ✅ Manuel tercih et
}
```

❌ **Yanlış parametreler** (çalışmaz):
- `subtitlesLanguage` → Doğrusu: `subtitleLang`
- `subtitlesFormat` → Dataset'te her zaman SRT formatında gelir

#### ✅ ÇÖZÜLDÜ: SRT Parse Etme

**Sorun:** Altyazılar SRT formatında geliyordu (zaman damgaları + metin)

**Çözüm:** `parse_srt_to_text()` fonksiyonu eklendi:
- Zaman damgalarını kaldırır (`00:00:00,000 --> ...`)
- Segment numaralarını atar
- Sadece altyazı metnini çıkarır

#### ✅ Nerede Bulunur?

Altyazılar **Dataset**'te, `item['subtitles']` listesinde:
```python
# Dataset'ten al
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    if 'subtitles' in item and item['subtitles']:
        subtitle_item = item['subtitles'][0]
        srt_content = subtitle_item['srt']  # SRT formatında tam altyazı
        # SRT'yi parse et
        plain_text = parse_srt_to_text(srt_content)
```

❌ **Key-Value Store'da DEĞİL** (sadece belirli ayarlarla)

#### Fallback Sistemi
- **Yeni özellik:** Apify başarısız olursa otomatik olarak youtube-transcript-api kullanılır
- Önce manuel altyazı, sonra otomatik oluşturulan altyazılar denenir
- Video ID formatının doğru olduğundan emin olun

#### ⚡ Hızlı Başlangıç
1. Apify ile İngilizce altyazıları çekin (SRT parse otomatik)
2. Direkt Gemini 2.5 Flash'a yükleyin
3. **Türkçe sohbet edin!** (çeviri gerekmez)

### Çeviri ile ilgili sorular

⚠️ **Artık Türkçe çeviri gerekmez!** Gemini 2.5 Flash:
- İngilizce altyazıları okuyup anlar
- Türkçe soru sorunca Türkçe cevap verir
- Daha hızlı ve daha ucuz (çeviri API maliyeti yok)

### Gemini yükleme hatası

#### ✅ ÇÖZÜLDÜ: `module 'google.generativeai' has no attribute 'upload_file'`

**Sorun:** Eski `google-generativeai` versiyonu (0.3.2) `upload_file()` fonksiyonunu desteklemiyor

**Çözüm:** Paketi güncelleyin:

```powershell
# Windows PowerShell / Linux / macOS
pip install --upgrade google-generativeai
```

**Gereken versiyon:** 0.8.0+ (Gemini File Search desteği için)

**Test edin:**
```powershell
python -c "import google.generativeai as genai; print(genai.__version__)"
```

#### Diğer Gemini hataları
- API anahtarının geçerli olduğundan emin olun
- Gemini API limitlerini kontrol edin (ücretsiz plan: 15 istek/dakika)
- İnternet bağlantınızı kontrol edin
- `.env` dosyasında `GEMINI_API_KEY` doğru yazıldığından emin olun

### 🪟 Windows PowerShell Sorunları

#### "python komutu bulunamadı"
```powershell
# Python'un PATH'e eklendiğinden emin olun
# Veya tam yol ile çalıştırın:
C:\Python311\python.exe main.py
```

#### "Activate.ps1 çalıştırılamıyor"
```powershell
# PowerShell'i Yönetici olarak açın:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Modül bulunamadı hatası
```powershell
# Paketleri tekrar yükleyin:
pip install --upgrade -r requirements.txt
```

#### Kurulumu test etme
```powershell
# Python versiyonu
python --version

# Paket kontrolü
python -c "import apify_client; print('Apify OK')"
python -c "import google.generativeai; print('Gemini OK')"
python -c "from youtube_transcript_api import YouTubeTranscriptApi; print('YouTube API OK')"
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Teşekkürler

- [Apify](https://apify.com/) - YouTube video ve altyazı çekme için
- [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) - Türkçe AI chat için
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) - Fallback altyazı sistemi için

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not:** Bu araç eğitim amaçlıdır. YouTube'un kullanım şartlarına uygun kullanın.
