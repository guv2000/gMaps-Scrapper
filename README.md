# gMaps-Scrapper

> **Not:** Google Maps kullanım şartları otomatik erişimi kısıtlayabilir. Bu aracı sorumlu şekilde ve yürürlükteki yasa/politikalara uygun olarak kullanın.

## Bu proje ne yapıyor?
Bu repo, **Python + Playwright** ile çalışan bir komut satırı aracı sağlar:
- Program çalışınca sana soru sorar: `şehir` ve `aranacak kelime` (ör. `fethiye` + `berber`).
- Google Maps sonuç listesini aşağı kaydırarak tüm firmaları yüklemeye çalışır.
- Her firma kartına girip detayları toplar.
- Uygunsa **tüm yorumları** ve **fotoğraf linklerini** çıkarır.
- Sonuçları CSV olarak kaydeder.

## Gereksinimler
- Python 3.10+
- Playwright tarayıcıları (Chromium)

## Kurulum
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
```

## Çalıştırma
```bash
python gmaps_scraper.py
```
Program sırasıyla şunları sorar:
- **Şehir/Bölge**: (ör. `fethiye`)
- **Arama kelimesi**: (ör. `berber`)
- **Çıktı klasörü**: (varsayılan `output`)

Çıktılar:
- `output/businesses.csv`
- `output/reviews.csv`
- `output/photos.csv`

## CSV Kolonları
### `businesses.csv`
- `business_id`, `name`, `address`, `phone`, `website`, `category`, `rating`, `review_count`, `hours`, `lat`, `lng`, `source_url`, `fetched_at`

### `reviews.csv`
- `business_id`, `review_id`, `reviewer`, `rating`, `date`, `text`

### `photos.csv`
- `business_id`, `photo_url`

## Hızlı Test (elle)
1. Komutu çalıştır: `python gmaps_scraper.py`
2. Örnek giriş ver:
   - Şehir/Bölge: `fethiye`
   - Arama kelimesi: `berber`
3. Tarayıcı açılacak ve sonuçlar toplanacak.
4. İş bitince `output/` klasöründeki CSV dosyalarını kontrol et.

## GitHub'a Yayınlama (kendi repo’n)
1. GitHub’da repo oluştur (boş repo).
2. Bu klasörde sırasıyla çalıştır:
```bash
git remote add origin https://github.com/KULLANICI_ADIN/REPO_ADI.git
git push -u origin main
```
> Eğer dal adı `main` değilse, `git branch` ile kontrol edip uygun dal adını yaz.

## GitHub'dan güncel kodu alma (public repo)
Senin repo adresin: `https://github.com/guv2000/gMaps-Scrapper`

### İlk kurulum (bilgisayarında hiç yoksa)
```bash
git clone https://github.com/guv2000/gMaps-Scrapper.git
cd gMaps-Scrapper
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
python gmaps_scraper.py
```

### Güncelleme (bilgisayarında zaten varsa)
```bash
cd gMaps-Scrapper
git pull
source .venv/bin/activate
pip install -r requirements.txt
python gmaps_scraper.py
```

## Ban riskini azaltmak için ipuçları
- Headed (görünür) mod zaten açık.
- Çok hızlı/çok paralel çekimden kaçın.
- Kısa aralıklarla ve makul hacimde çalıştır.

## Sorumluluk
Bu araç, meşru veri toplama amaçları içindir. Rehber siten için veriyi kullanma hakkın olduğundan emin ol.
