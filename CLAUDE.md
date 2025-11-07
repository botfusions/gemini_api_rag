YouTube kanalları için bir araç yap:
- Kullanıcıdan kanal URL'si iste
- Videolar en yeniden eskiye doğru sıralansın
- Apify kullanarak video başlıkları ve altyazıları çek
- Her video için ayrı dosya oluştur
- Gemini API File Search'e ekle
- Alt YAzılar için Chat arayüzü oluştur
- tr çıktı ver
I want you to build a RAG tool for any YouTube channel ... ask me the Channel URL and how many videos to store from newest to older. You'll then use Apify to grab the video title and subtitles, create a file for each video that you'll add to Gemini API

You'll need to store .env vars for Gemini API and Apify API.

Apify actor to use: https://apify.com/streamers/youtube-scraper.md

Doc links below: https://ai.google.dev/gemini-api/docs/file-search https://docs.apify.com/llms.txt
