# LexTrack — Hukuk Bürosu Dava Takip Sistemi

**BTS304 Veritabanı Yönetim Sistemleri II — Final Ödevi**
Python (PyQt5) + MySQL ile geliştirilmiş masaüstü uygulaması.

---

## 🎯 Özellikler

- Müşteri, Avukat, Dava, Duruşma, Belge, Masraf, Ödeme, Görev yönetimi
- N-Katmanlı mimari (DAL → BLL → UI)
- Tüm veritabanı işlemleri Stored Procedure üzerinden yapılır
- 8 Tablo, 30+ Stored Procedure, 3 View, 3 Trigger, 2 Function, 2 Transaction prosedürü

---

## 📋 Gereksinimler

Bilgisayarınızda şunların kurulu olması gerekir:

- **Python 3.10 veya üstü** → https://www.python.org/downloads/
- **MySQL Server 8.0+** → https://dev.mysql.com/downloads/
- **MySQL Workbench** (veritabanını kurmak için)
- Bir kod editörü (VS Code önerilir) → https://code.visualstudio.com/

---

## ⚙️ KURULUM (Adım Adım)

### ADIM 1 — Projeyi İndir

**Yöntem A (Kolay — ZIP):**
1. Bu sayfanın üstündeki yeşil **`< > Code`** butonuna tıklayın
2. Açılan menüden **Download ZIP** seçin
3. İnen ZIP dosyasına sağ tıklayıp **Tümünü Ayıkla / Extract All** deyin
4. Bir klasöre çıkarın (örn: Masaüstü)

**Yöntem B (Git ile):**
```bash
git clone https://github.com/KULLANICI_ADI/lextrack.git
```

---

### ADIM 2 — Projeyi VS Code'da Aç

1. **VS Code**'u açın
2. **File → Open Folder** (Dosya → Klasör Aç)
3. ZIP'ten çıkardığınız **`lextrack`** klasörünü seçin
4. Sol tarafta proje dosyalarını göreceksiniz:

```
lextrack/
├── main.py                ← Uygulamayı başlatan dosya
├── config.py              ← Veritabanı ayarları (ŞİFRE BURAYA)
├── requirements.txt       ← Python kütüphaneleri
├── README.md              ← Bu dosya
├── database/
│   └── hukuk_burosu.sql   ← ⭐ VERİTABANI DOSYASI BURADA
├── dal/                   ← Veri Erişim Katmanı
├── bll/                   ← İş Katmanı
└── ui/                    ← Arayüz Katmanı
```

---

### ADIM 3 — Veritabanını Oluştur (MySQL Workbench)

1. **MySQL Workbench**'i açın ve bağlantınıza tıklayın (şifrenizi girin)
2. Üst menüden **File → Open SQL Script** tıklayın
3. Proje klasöründeki şu dosyayı seçin:
   ```
   lextrack/database/hukuk_burosu.sql
   ```
4. Dosya açıldıktan sonra üstteki **⚡ (yıldırım / Execute)** butonuna tıklayın
5. Alttaki **Output** panelinde yeşil tikler görünmeli (hata yoksa tamamdır)
6. Bu işlem şunları otomatik oluşturur:
   - Veritabanı (`hukuk_burosu`)
   - 8 tablo
   - 30+ stored procedure
   - 3 trigger, 2 function, 3 view, 2 transaction prosedürü
   - Örnek veriler (8 avukat, 18 müşteri, 22 dava vb.)

> **Kontrol:** Sol paneldeki **Schemas** kısmında `hukuk_burosu` veritabanını görmelisiniz. Görmüyorsanız sağ tık → **Refresh All**.

---

### ADIM 4 — Veritabanı Bağlantı Ayarı

1. VS Code'da **`config.py`** dosyasını açın
2. MySQL şifrenizi `DB_PASSWORD` satırına yazın:

```python
class Config:
    DB_HOST     = 'localhost'
    DB_PORT     = 3306
    DB_USER     = 'root'
    DB_PASSWORD = 'MYSQL_SIFRENIZI_BURAYA_YAZIN'    # ← buraya
    DB_NAME     = 'hukuk_burosu'
    DB_CHARSET  = 'utf8mb4'
    SECRET_KEY  = 'lextrack-secret-2026'
```

3. Dosyayı kaydedin (**Ctrl+S**)

---

### ADIM 5 — Python Kütüphanelerini Kur

VS Code'da **Terminal → New Terminal** açın ve şunu yazın:

```bash
pip install -r requirements.txt
```

Bu komut PyQt5 ve mysql-connector-python kütüphanelerini kurar.

---

### ADIM 6 — Uygulamayı Çalıştır

Aynı terminalde:

```bash
python main.py
```

Uygulama açılır. Dashboard'da istatistikler ve örnek veriler görünür. 🎉

---

## 🛠️ Sık Karşılaşılan Sorunlar

| Hata | Çözüm |
|------|-------|
| `Unknown database 'hukuk_burosu'` | ADIM 3'ü yapmadınız — SQL dosyasını Workbench'te çalıştırın |
| `Access denied for user 'root'` | `config.py`'de şifre yanlış — doğru MySQL şifrenizi yazın |
| `No module named 'PyQt5'` | `pip install -r requirements.txt` komutunu çalıştırın |
| `Can't connect to MySQL server` | MySQL Server çalışmıyor — servisi başlatın |

---

## 🏛️ Mimari (N-Katmanlı)

| Katman | Klasör | Sorumluluk |
|--------|--------|-----------|
| **Sunum (UI)** | `ui/` | PyQt5 pencereleri ve formları |
| **İş (BLL)** | `bll/` | Doğrulama ve iş kuralları |
| **Veri Erişim (DAL)** | `dal/` | Sadece Stored Procedure çağrıları |

> **Önemli kural:** Hiçbir katmanda doğrudan SQL kodu (SELECT/INSERT/UPDATE/DELETE) yoktur. Tüm veritabanı işlemleri DAL katmanında **Stored Procedure** ile yapılır.

---

## 🗄️ Veritabanı İçeriği

- **Tablolar:** avukatlar, musteriler, davalar, durusmalar, belgeler, masraflar, odemeler, gorevler
- **Function:** `fn_DavaMasrafToplam`, `fn_MusteriOdemeToplam`
- **Trigger:** `tg_durusma_sonuc_kaydet`, `tg_gorev_gecikme_kontrol`, `tg_dava_sil_kontrol`
- **View:** `view_aktif_davalar`, `view_musteri_mali_ozet`, `view_yaklasan_durusmalar`
- **Transaction:** `sp_DavaKapat`, `sp_MusteriVeDavaEkle`

---

## 👤 Geliştirici

**[Umut Kağan Ceylan]** — [23010708011]
Bartın Üniversitesi — Bilgisayar Teknolojisi ve Bilişim Sistemleri Bölümü
