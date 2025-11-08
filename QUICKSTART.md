# ⚡ Hızlı Başlangıç Rehberi

Bu rehber, YouTube Kanal Analiz Aracı'nı 5 dakikada çalıştırmanıza yardımcı olacak.

## 🎯 3 Adımda Başlayın

### 1️⃣ Kurulum

```bash
bash setup.sh
```

Bu script:
- Python versiyonunu kontrol eder
- Virtual environment oluşturur (isteğe bağlı)
- Gerekli paketleri yükler
- `.env` dosyasını oluşturur

### 2️⃣ API Anahtarlarını Ekleyin

`.env` dosyasını düzenleyin:

```bash
nano .env
```

veya favori editörünüzle açın ve API anahtarlarınızı ekleyin:

```env
APIFY_API_KEY=your_actual_apify_key
GEMINI_API_KEY=your_actual_gemini_key
```

#### 🔑 API Anahtarları Nereden Alınır?

**Apify API:**
1. https://apify.com/ adresine gidin
2. Ücretsiz hesap oluşturun
3. Settings → Integrations → API Token
4. Token'ı kopyalayıp `.env` dosyasına yapıştırın

**Gemini API:**
1. https://makersuite.google.com/app/apikey adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. API Key'i kopyalayıp `.env` dosyasına yapıştırın

### 3️⃣ Çalıştırın

```bash
bash run.sh
```

veya doğrudan:

```bash
python main.py
```

## 📖 İlk Kullanım

Program başladığında interaktif menü göreceksiniz:

```
=== YouTube Kanal Analiz Aracı ===

1. Yeni kanal analiz et
2. Mevcut videoları Türkçe'ye çevir
3. Videoları Gemini'ye yükle
4. Chat'i başlat
5. Tüm işlemleri sırayla yap
6. Çıkış

Seçiminiz (1-6):
```

### 🎬 İlk Kez Kullanım İçin

İlk kez kullanıyorsanız **5. Tüm işlemleri sırayla yap** seçeneğini seçin:

1. YouTube kanal URL'si girin (örn: `https://www.youtube.com/@channelname`)
2. Kaç video çekmek istediğinizi belirtin (örn: `10`)
3. Bekleyin - tüm işlemler otomatik yapılacak:
   - Videolar çekilir
   - Altyazılar Türkçe'ye çevrilir
   - Gemini'ye yüklenir
   - Chat başlatılır

## 💬 Chat Kullanımı

Chat başladığında videolarınız hakkında Türkçe sorular sorabilirsiniz:

**Örnek sorular:**
- "Kaç video var?"
- "En popüler video hangisi?"
- "Python hakkında hangi videolar var?"
- "Son videoda ne anlatılmış?"
- "En çok hangi konular işlenmiş?"

**Komutlar:**
- `çıkış` veya `q` - Chat'ten çık
- `yardım` veya `h` - Yardım göster
- `temizle` veya `c` - Ekranı temizle

## 🔄 Sonraki Kullanımlar

Zaten videoları çektiyseniz ve sadece chat yapmak istiyorsanız:

1. `python main.py` çalıştırın
2. Menüden **4. Chat'i başlat** seçin

## 📁 Dosya Yapısı

Çalıştırdıktan sonra:

```
gemini_api_rag/
├── videos/
│   ├── videoID1.json    # Video 1 verisi
│   ├── videoID2.json    # Video 2 verisi
│   └── temp_docs/       # Gemini için geçici dosyalar
├── .env                  # API anahtarlarınız (GİZLİ)
└── venv/                 # Virtual environment (opsiyonel)
```

## ⚠️ Sorun mu Yaşıyorsunuz?

### "ModuleNotFoundError" hatası
```bash
pip install -r requirements.txt
```

### "APIFY_API_KEY bulunamadı" hatası
- `.env` dosyasının proje ana dizininde olduğundan emin olun
- API anahtarlarının doğru girildiğini kontrol edin

### Videolar çekilmiyor
- Kanal URL'inin doğru olduğundan emin olun
- Kanalın herkese açık olduğunu kontrol edin
- Apify hesabınızın aktif olduğunu kontrol edin

### Virtual environment sorunları
Virtual environment kullanmadan da çalıştırabilirsiniz:
```bash
python main.py
```

## 🎓 Daha Fazla Bilgi

Detaylı dokümantasyon için [README.md](README.md) dosyasına bakın.

## 🚀 Hızlı Referans

```bash
# Kurulum
bash setup.sh

# Çalıştırma
bash run.sh
# veya
python main.py

# Sadece video çek
python youtube_scraper.py

# Sadece çevir
python translator.py

# Sadece chat
python chat.py
```

---

**İyi kullanımlar! 🎉**
