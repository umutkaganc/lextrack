# LexTrack — Hukuk Bürosu Dava Takip Sistemi

BTS304 Veritabanı Yönetim Sistemleri II — Final Ödevi
Python (PyQt5) + MySQL ile geliştirilmiş masaüstü uygulaması.

---

## 🎯 Özellikler

- Müşteri, Avukat, Dava, Duruşma, Belge, Masraf, Ödeme, Görev yönetimi
- N-Katmanlı mimari (DAL → BLL → UI)
- Tüm veritabanı işlemleri Stored Procedure üzerinden
- 3 View, 3 Trigger, 2 Function, 2 Transaction prosedürü

---

## 📋 Gereksinimler

- Python 3.10+
- MySQL Server 8.0+
- MySQL Workbench (veritabanını kurmak için)

---

## ⚙️ Kurulum

### 1. Projeyi indir

**Yöntem A — ZIP olarak (kolay):**
GitHub'da yeşil **Code** butonuna tıkla → **Download ZIP** → indir → klasöre çıkart

**Yöntem B — Git ile:**
```bash
git clone https://github.com/KULLANICI_ADI/lextrack-hukuk-sistemi.git
cd lextrack-hukuk-sistemi
```

### 2. Python kütüphanelerini kur
```bash
pip install -r requirements.txt
```

### 3. Veritabanını oluştur
MySQL Workbench'i aç:
- **File → Open SQL Script** → `database/hukuk_burosu.sql` seç
- **⚡ (Execute)** butonuna tıkla
- Veritabanı, tablolar, stored procedure'ler, trigger'lar, view'ler ve örnek veriler otomatik oluşur

### 4. Bağlantı ayarlarını yap
`config.py` dosyasını aç, MySQL şifreni gir:
```python
class Config:
    DB_HOST     = 'localhost'
    DB_PORT     = 3306
    DB_USER     = 'root'
    DB_PASSWORD = 'BURAYA_MYSQL_SIFRENI_YAZ'
    DB_NAME     = 'hukuk_burosu'
```

### 5. Uygulamayı çalıştır
```bash
python main.py
```

---

## 🗂️ Proje Yapısı

```
lextrack/
├── main.py                  # Başlangıç noktası
├── config.py                # Veritabanı ayarları
├── requirements.txt         # Python kütüphaneleri
├── database/
│   └── hukuk_burosu_TEMIZ.sql   # Veritabanı scripti (tek dosya)
├── dal/                     # Veri Erişim Katmanı (Stored Procedure çağrıları)
│   ├── db.py
│   ├── avukat_dal.py
│   ├── musteri_dal.py
│   ├── dava_dal.py
│   └── ...
├── bll/                     # İş Katmanı (doğrulama, iş kuralları)
│   └── services.py
└── ui/                      # Sunum Katmanı (PyQt5 arayüz)
    ├── main_window.py
    ├── dashboard_ui.py
    └── ...
```

---

## 🏛️ Mimari

| Katman | Sorumluluk |
|--------|-----------|
| **UI (Sunum)** | PyQt5 pencereleri ve formları |
| **BLL (İş)** | Doğrulama ve iş kuralları |
| **DAL (Veri Erişim)** | Sadece Stored Procedure çağrıları |

> **Önemli:** Hiçbir katmanda doğrudan SQL kodu (SELECT/INSERT/UPDATE/DELETE) yoktur. Tüm veritabanı işlemleri DAL katmanında Stored Procedure ile yapılır.

---

## 👤 Geliştirici

[Umut Kağan Ceylan] — [23010708011]
Bartın Üniversitesi — Bilgisayar Teknolojisi ve Bilişim Sistemleri
