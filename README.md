# LexTrack — Hukuk Bürosu Dava Takip Sistemi
BTS304 Final Ödevi — PyQt5 Masaüstü Uygulaması

## Kurulum

### 1. Bağımlılıkları Kur
```
pip install -r requirements.txt
```

### 2. Veritabanını Oluştur
MySQL Workbench veya komut satırı ile:
```
SOURCE database/hukuk_burosu.sql
```

### 3. Bağlantı Ayarları
`config.py` dosyasını açın ve MySQL bilgilerinizi girin:
```python
DB_PASSWORD = 'mysql_sifreniz'
```

### 4. Uygulamayı Çalıştır
```
python main.py
```

## Mimari
```
lextrack/
├── main.py               → Giriş noktası
├── config.py             → Veritabanı ayarları
├── dal/                  → Veri Erişim Katmanı (DAL)
│   ├── db.py             → MySQL bağlantısı
│   └── *_dal.py          → Stored Procedure çağrıları
├── bll/                  → İş Katmanı (BLL)
│   └── services.py       → Doğrulama ve iş kuralları
├── ui/                   → Sunum Katmanı (PL)
│   ├── main_window.py    → Ana pencere
│   ├── *_ui.py           → CRUD arayüzleri
│   └── style.py          → QSS stilleri
└── database/
    └── hukuk_burosu.sql  → Veritabanı scripti
```
