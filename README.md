# Amazon Ürün Scraper

Bu Python scripti, Amazon Türkiye'den ürün bilgilerini çekmek için tasarlanmış bir web scraper'dır.

## Özellikler

- Anahtar kelimeye göre ürün arama
- Birden fazla sayfa tarama desteği
- Ürün bilgilerini JSON formatında kaydetme
- Rate limiting ile güvenli scraping
- Hata yönetimi
- Rastgele User-Agent kullanımı

## Çekilen Ürün Bilgileri

- ASIN (Amazon Standard Identification Number)
- Ürün başlığı
- Fiyat
- Yıldız değerlendirmesi
- Değerlendirme sayısı
- Ürün URL'i

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

Scripti çalıştırmak için:
```bash
python amazon_scraper.py
```

Program sizden:
1. Aramak istediğiniz ürünü
2. Taramak istediğiniz sayfa sayısını

isteyecektir.

Sonuçlar `amazon_products.json` dosyasına kaydedilecektir.

## Notlar

- Amazon'un bot politikalarına uygun olarak 2 saniye aralıklarla istekler yapılmaktadır
- Scraping yaparken Amazon'un kullanım koşullarını göz önünde bulundurun
- Çok fazla istek göndermekten kaçının