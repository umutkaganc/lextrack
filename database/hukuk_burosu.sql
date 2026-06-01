-- ============================================================
-- HUKUK BÜROSU DAVA TAKİP SİSTEMİ - VERİTABANI
-- BTS304 - Veritabanı Yönetim Sistemleri II
-- ============================================================

CREATE DATABASE IF NOT EXISTS hukuk_burosu
  CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci;

USE hukuk_burosu;

-- ============================================================
-- TABLO OLUŞTURMA
-- ============================================================

-- 1. AVUKATLAR
CREATE TABLE IF NOT EXISTS avukatlar (
    avukat_id   INT             NOT NULL AUTO_INCREMENT,
    ad          VARCHAR(64)     NOT NULL,
    soyad       VARCHAR(64)     NOT NULL,
    baro_no     VARCHAR(30)     NOT NULL UNIQUE,
    uzmanlik    VARCHAR(100)    NOT NULL DEFAULT 'Genel Hukuk',
    telefon     VARCHAR(20)     NOT NULL,
    email       VARCHAR(100)    NOT NULL UNIQUE,
    aktif       TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (avukat_id)
);

-- 2. MÜŞTERİLER
CREATE TABLE IF NOT EXISTS musteriler (
    musteri_id      INT             NOT NULL AUTO_INCREMENT,
    ad              VARCHAR(64)     NOT NULL,
    soyad           VARCHAR(64)     NOT NULL,
    tc_no           VARCHAR(11)     NOT NULL UNIQUE,
    telefon         VARCHAR(20)     NOT NULL,
    email           VARCHAR(100),
    adres           VARCHAR(250),
    kayit_tarihi    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (musteri_id)
);

-- 3. DAVALAR
CREATE TABLE IF NOT EXISTS davalar (
    dava_id         INT             NOT NULL AUTO_INCREMENT,
    musteri_id      INT             NOT NULL,
    avukat_id       INT             NOT NULL,
    dava_no         VARCHAR(50)     NOT NULL UNIQUE,
    dava_turu       VARCHAR(100)    NOT NULL,
    mahkeme         VARCHAR(200)    NOT NULL,
    acilis_tarihi   DATE            NOT NULL DEFAULT (CURDATE()),
    durum           ENUM('Aktif','Kazanildi','Kaybedildi','Uzlasma','Durduruldu')
                    NOT NULL DEFAULT 'Aktif',
    aciklama        VARCHAR(1000),
    PRIMARY KEY (dava_id),
    FOREIGN KEY (musteri_id) REFERENCES musteriler(musteri_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (avukat_id) REFERENCES avukatlar(avukat_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 4. DURUŞMALAR
CREATE TABLE IF NOT EXISTS durusmalar (
    durusma_id      INT             NOT NULL AUTO_INCREMENT,
    dava_id         INT             NOT NULL,
    durusma_tarihi  DATETIME        NOT NULL,
    sonuc           VARCHAR(500),
    notlar          VARCHAR(1000),
    durum           ENUM('Planlandi','Tamamlandi','Ertelendi') NOT NULL DEFAULT 'Planlandi',
    PRIMARY KEY (durusma_id),
    FOREIGN KEY (dava_id) REFERENCES davalar(dava_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 5. BELGELER
CREATE TABLE IF NOT EXISTS belgeler (
    belge_id            INT             NOT NULL AUTO_INCREMENT,
    dava_id             INT             NOT NULL,
    belge_adi           VARCHAR(200)    NOT NULL,
    belge_turu          VARCHAR(100)    NOT NULL DEFAULT 'Diger',
    aciklama            VARCHAR(500),
    yuklenme_tarihi     DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (belge_id),
    FOREIGN KEY (dava_id) REFERENCES davalar(dava_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 6. MASRAFLAR
CREATE TABLE IF NOT EXISTS masraflar (
    masraf_id   INT             NOT NULL AUTO_INCREMENT,
    dava_id     INT             NOT NULL,
    aciklama    VARCHAR(300)    NOT NULL,
    tutar       DECIMAL(10,2)   NOT NULL DEFAULT 0,
    tarih       DATE            NOT NULL DEFAULT (CURDATE()),
    tur         VARCHAR(100)    NOT NULL DEFAULT 'Diger',
    CONSTRAINT chk_masraf_tutar CHECK (tutar >= 0),
    PRIMARY KEY (masraf_id),
    FOREIGN KEY (dava_id) REFERENCES davalar(dava_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 7. ÖDEMELER
CREATE TABLE IF NOT EXISTS odemeler (
    odeme_id        INT             NOT NULL AUTO_INCREMENT,
    musteri_id      INT             NOT NULL,
    dava_id         INT             NOT NULL,
    tutar           DECIMAL(10,2)   NOT NULL DEFAULT 0,
    tarih           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tur             ENUM('Nakit','Kredi Karti','Banka Transferi','Cek') NOT NULL DEFAULT 'Nakit',
    aciklama        VARCHAR(300),
    CONSTRAINT chk_odeme_tutar CHECK (tutar > 0),
    PRIMARY KEY (odeme_id),
    FOREIGN KEY (musteri_id) REFERENCES musteriler(musteri_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (dava_id) REFERENCES davalar(dava_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 8. GÖREVLER
CREATE TABLE IF NOT EXISTS gorevler (
    gorev_id        INT             NOT NULL AUTO_INCREMENT,
    dava_id         INT             NOT NULL,
    avukat_id       INT             NOT NULL,
    aciklama        VARCHAR(500)    NOT NULL,
    son_tarih       DATE,
    durum           ENUM('Bekliyor','Devam Ediyor','Tamamlandi','Iptal') NOT NULL DEFAULT 'Bekliyor',
    olusturma_tarihi DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (gorev_id),
    FOREIGN KEY (dava_id) REFERENCES davalar(dava_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (avukat_id) REFERENCES avukatlar(avukat_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- STORED PROCEDURES - AVUKATLAR
-- ============================================================

DELIMITER $$

CREATE PROCEDURE sp_AvukatEkle(
    IN p_ad         VARCHAR(64),
    IN p_soyad      VARCHAR(64),
    IN p_baro_no    VARCHAR(30),
    IN p_uzmanlik   VARCHAR(100),
    IN p_telefon    VARCHAR(20),
    IN p_email      VARCHAR(100)
)
BEGIN
    INSERT INTO avukatlar(ad, soyad, baro_no, uzmanlik, telefon, email)
    VALUES(p_ad, p_soyad, p_baro_no, p_uzmanlik, p_telefon, p_email);
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_AvukatGuncelle(
    IN p_id         INT,
    IN p_ad         VARCHAR(64),
    IN p_soyad      VARCHAR(64),
    IN p_baro_no    VARCHAR(30),
    IN p_uzmanlik   VARCHAR(100),
    IN p_telefon    VARCHAR(20),
    IN p_email      VARCHAR(100),
    IN p_aktif      TINYINT(1)
)
BEGIN
    UPDATE avukatlar
    SET ad=p_ad, soyad=p_soyad, baro_no=p_baro_no, uzmanlik=p_uzmanlik,
        telefon=p_telefon, email=p_email, aktif=p_aktif
    WHERE avukat_id = p_id;
END $$

CREATE PROCEDURE sp_AvukatSil(IN p_id INT)
BEGIN
    DELETE FROM avukatlar WHERE avukat_id = p_id;
END $$

CREATE PROCEDURE sp_AvukatListele()
BEGIN
    SELECT avukat_id, ad, soyad, baro_no, uzmanlik, telefon, email, aktif
    FROM avukatlar ORDER BY soyad, ad;
END $$

CREATE PROCEDURE sp_AvukatGetir(IN p_id INT)
BEGIN
    SELECT avukat_id, ad, soyad, baro_no, uzmanlik, telefon, email, aktif
    FROM avukatlar WHERE avukat_id = p_id;
END $$

-- ============================================================
-- STORED PROCEDURES - MÜŞTERİLER
-- ============================================================

CREATE PROCEDURE sp_MusteriEkle(
    IN p_ad         VARCHAR(64),
    IN p_soyad      VARCHAR(64),
    IN p_tc_no      VARCHAR(11),
    IN p_telefon    VARCHAR(20),
    IN p_email      VARCHAR(100),
    IN p_adres      VARCHAR(250)
)
BEGIN
    INSERT INTO musteriler(ad, soyad, tc_no, telefon, email, adres)
    VALUES(p_ad, p_soyad, p_tc_no, p_telefon, p_email, p_adres);
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_MusteriGuncelle(
    IN p_id         INT,
    IN p_ad         VARCHAR(64),
    IN p_soyad      VARCHAR(64),
    IN p_tc_no      VARCHAR(11),
    IN p_telefon    VARCHAR(20),
    IN p_email      VARCHAR(100),
    IN p_adres      VARCHAR(250)
)
BEGIN
    UPDATE musteriler
    SET ad=p_ad, soyad=p_soyad, tc_no=p_tc_no,
        telefon=p_telefon, email=p_email, adres=p_adres
    WHERE musteri_id = p_id;
END $$

CREATE PROCEDURE sp_MusteriSil(IN p_id INT)
BEGIN
    DELETE FROM musteriler WHERE musteri_id = p_id;
END $$

CREATE PROCEDURE sp_MusteriListele()
BEGIN
    SELECT musteri_id, ad, soyad, tc_no, telefon, email, adres, kayit_tarihi
    FROM musteriler ORDER BY soyad, ad;
END $$

CREATE PROCEDURE sp_MusteriGetir(IN p_id INT)
BEGIN
    SELECT musteri_id, ad, soyad, tc_no, telefon, email, adres, kayit_tarihi
    FROM musteriler WHERE musteri_id = p_id;
END $$

-- ============================================================
-- STORED PROCEDURES - DAVALAR
-- ============================================================

CREATE PROCEDURE sp_DavaEkle(
    IN p_musteri_id     INT,
    IN p_avukat_id      INT,
    IN p_dava_no        VARCHAR(50),
    IN p_dava_turu      VARCHAR(100),
    IN p_mahkeme        VARCHAR(200),
    IN p_acilis_tarihi  DATE,
    IN p_aciklama       VARCHAR(1000)
)
BEGIN
    INSERT INTO davalar(musteri_id, avukat_id, dava_no, dava_turu, mahkeme, acilis_tarihi, aciklama)
    VALUES(p_musteri_id, p_avukat_id, p_dava_no, p_dava_turu, p_mahkeme, p_acilis_tarihi, p_aciklama);
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_DavaGuncelle(
    IN p_id             INT,
    IN p_musteri_id     INT,
    IN p_avukat_id      INT,
    IN p_dava_no        VARCHAR(50),
    IN p_dava_turu      VARCHAR(100),
    IN p_mahkeme        VARCHAR(200),
    IN p_durum          VARCHAR(30),
    IN p_aciklama       VARCHAR(1000)
)
BEGIN
    UPDATE davalar
    SET musteri_id=p_musteri_id, avukat_id=p_avukat_id, dava_no=p_dava_no,
        dava_turu=p_dava_turu, mahkeme=p_mahkeme, durum=p_durum, aciklama=p_aciklama
    WHERE dava_id = p_id;
END $$

CREATE PROCEDURE sp_DavaSil(IN p_id INT)
BEGIN
    DELETE FROM davalar WHERE dava_id = p_id;
END $$

CREATE PROCEDURE sp_DavaListele()
BEGIN
    SELECT d.dava_id, d.dava_no, d.dava_turu, d.mahkeme, d.acilis_tarihi, d.durum, d.aciklama,
           m.musteri_id, CONCAT(m.ad,' ',m.soyad) AS musteri_adi, m.telefon AS musteri_tel,
           a.avukat_id, CONCAT(a.ad,' ',a.soyad) AS avukat_adi, a.uzmanlik
    FROM davalar d
    INNER JOIN musteriler m ON d.musteri_id = m.musteri_id
    INNER JOIN avukatlar a ON d.avukat_id = a.avukat_id
    ORDER BY d.acilis_tarihi DESC;
END $$

CREATE PROCEDURE sp_DavaGetir(IN p_id INT)
BEGIN
    SELECT d.dava_id, d.dava_no, d.dava_turu, d.mahkeme, d.acilis_tarihi, d.durum, d.aciklama,
           d.musteri_id, CONCAT(m.ad,' ',m.soyad) AS musteri_adi, m.telefon AS musteri_tel,
           d.avukat_id, CONCAT(a.ad,' ',a.soyad) AS avukat_adi
    FROM davalar d
    INNER JOIN musteriler m ON d.musteri_id = m.musteri_id
    INNER JOIN avukatlar a ON d.avukat_id = a.avukat_id
    WHERE d.dava_id = p_id;
END $$

-- ============================================================
-- STORED PROCEDURES - DURUŞMALAR
-- ============================================================

CREATE PROCEDURE sp_DurusmaEkle(
    IN p_dava_id    INT,
    IN p_tarih      DATETIME,
    IN p_notlar     VARCHAR(1000)
)
BEGIN
    INSERT INTO durusmalar(dava_id, durusma_tarihi, notlar, durum)
    VALUES(p_dava_id, p_tarih, p_notlar, 'Planlandi');
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_DurusmaGuncelle(
    IN p_id     INT,
    IN p_tarih  DATETIME,
    IN p_sonuc  VARCHAR(500),
    IN p_notlar VARCHAR(1000),
    IN p_durum  VARCHAR(20)
)
BEGIN
    UPDATE durusmalar
    SET durusma_tarihi=p_tarih, sonuc=p_sonuc, notlar=p_notlar, durum=p_durum
    WHERE durusma_id = p_id;
END $$

CREATE PROCEDURE sp_DurusmaSil(IN p_id INT)
BEGIN
    DELETE FROM durusmalar WHERE durusma_id = p_id;
END $$

CREATE PROCEDURE sp_DurusmaListele()
BEGIN
    SELECT dr.durusma_id, dr.durusma_tarihi, dr.sonuc, dr.notlar, dr.durum,
           d.dava_id, d.dava_no, d.dava_turu,
           CONCAT(m.ad,' ',m.soyad) AS musteri_adi
    FROM durusmalar dr
    INNER JOIN davalar d ON dr.dava_id = d.dava_id
    INNER JOIN musteriler m ON d.musteri_id = m.musteri_id
    ORDER BY dr.durusma_tarihi DESC;
END $$

CREATE PROCEDURE sp_DavaDurusmalari(IN p_dava_id INT)
BEGIN
    SELECT durusma_id, durusma_tarihi, sonuc, notlar, durum
    FROM durusmalar WHERE dava_id = p_dava_id
    ORDER BY durusma_tarihi DESC;
END $$

-- ============================================================
-- STORED PROCEDURES - BELGELER
-- ============================================================

CREATE PROCEDURE sp_BelgeEkle(
    IN p_dava_id    INT,
    IN p_belge_adi  VARCHAR(200),
    IN p_belge_turu VARCHAR(100),
    IN p_aciklama   VARCHAR(500)
)
BEGIN
    INSERT INTO belgeler(dava_id, belge_adi, belge_turu, aciklama)
    VALUES(p_dava_id, p_belge_adi, p_belge_turu, p_aciklama);
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_BelgeGuncelle(
    IN p_id         INT,
    IN p_belge_adi  VARCHAR(200),
    IN p_belge_turu VARCHAR(100),
    IN p_aciklama   VARCHAR(500)
)
BEGIN
    UPDATE belgeler
    SET belge_adi=p_belge_adi, belge_turu=p_belge_turu, aciklama=p_aciklama
    WHERE belge_id = p_id;
END $$

CREATE PROCEDURE sp_BelgeSil(IN p_id INT)
BEGIN
    DELETE FROM belgeler WHERE belge_id = p_id;
END $$

CREATE PROCEDURE sp_DavaBelgeleri(IN p_dava_id INT)
BEGIN
    SELECT belge_id, belge_adi, belge_turu, aciklama, yuklenme_tarihi
    FROM belgeler WHERE dava_id = p_dava_id
    ORDER BY yuklenme_tarihi DESC;
END $$

-- ============================================================
-- STORED PROCEDURES - MASRAFLAR
-- ============================================================

CREATE PROCEDURE sp_MasrafEkle(
    IN p_dava_id    INT,
    IN p_aciklama   VARCHAR(300),
    IN p_tutar      DECIMAL(10,2),
    IN p_tarih      DATE,
    IN p_tur        VARCHAR(100)
)
BEGIN
    INSERT INTO masraflar(dava_id, aciklama, tutar, tarih, tur)
    VALUES(p_dava_id, p_aciklama, p_tutar, p_tarih, p_tur);
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_MasrafGuncelle(
    IN p_id         INT,
    IN p_aciklama   VARCHAR(300),
    IN p_tutar      DECIMAL(10,2),
    IN p_tarih      DATE,
    IN p_tur        VARCHAR(100)
)
BEGIN
    UPDATE masraflar
    SET aciklama=p_aciklama, tutar=p_tutar, tarih=p_tarih, tur=p_tur
    WHERE masraf_id = p_id;
END $$

CREATE PROCEDURE sp_MasrafSil(IN p_id INT)
BEGIN
    DELETE FROM masraflar WHERE masraf_id = p_id;
END $$

CREATE PROCEDURE sp_DavaMasraflari(IN p_dava_id INT)
BEGIN
    SELECT masraf_id, aciklama, tutar, tarih, tur
    FROM masraflar WHERE dava_id = p_dava_id
    ORDER BY tarih DESC;
END $$

-- ============================================================
-- STORED PROCEDURES - ÖDEMELER
-- ============================================================

CREATE PROCEDURE sp_OdemeEkle(
    IN p_musteri_id INT,
    IN p_dava_id    INT,
    IN p_tutar      DECIMAL(10,2),
    IN p_tur        VARCHAR(30),
    IN p_aciklama   VARCHAR(300)
)
BEGIN
    INSERT INTO odemeler(musteri_id, dava_id, tutar, tur, aciklama)
    VALUES(p_musteri_id, p_dava_id, p_tutar, p_tur, p_aciklama);
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_OdemeGuncelle(
    IN p_id     INT,
    IN p_tutar  DECIMAL(10,2),
    IN p_tur    VARCHAR(30),
    IN p_aciklama VARCHAR(300)
)
BEGIN
    UPDATE odemeler
    SET tutar=p_tutar, tur=p_tur, aciklama=p_aciklama
    WHERE odeme_id = p_id;
END $$

CREATE PROCEDURE sp_OdemeSil(IN p_id INT)
BEGIN
    DELETE FROM odemeler WHERE odeme_id = p_id;
END $$

CREATE PROCEDURE sp_OdemeListele()
BEGIN
    SELECT o.odeme_id, o.tutar, o.tarih, o.tur, o.aciklama,
           CONCAT(m.ad,' ',m.soyad) AS musteri_adi,
           d.dava_no, d.dava_turu
    FROM odemeler o
    INNER JOIN musteriler m ON o.musteri_id = m.musteri_id
    INNER JOIN davalar d ON o.dava_id = d.dava_id
    ORDER BY o.tarih DESC;
END $$

CREATE PROCEDURE sp_DavaOdemeleri(IN p_dava_id INT)
BEGIN
    SELECT o.odeme_id, o.tutar, o.tarih, o.tur, o.aciklama,
           CONCAT(m.ad,' ',m.soyad) AS musteri_adi
    FROM odemeler o
    INNER JOIN musteriler m ON o.musteri_id = m.musteri_id
    WHERE o.dava_id = p_dava_id
    ORDER BY o.tarih DESC;
END $$

-- ============================================================
-- STORED PROCEDURES - GÖREVLER
-- ============================================================

CREATE PROCEDURE sp_GorevEkle(
    IN p_dava_id    INT,
    IN p_avukat_id  INT,
    IN p_aciklama   VARCHAR(500),
    IN p_son_tarih  DATE
)
BEGIN
    INSERT INTO gorevler(dava_id, avukat_id, aciklama, son_tarih, durum)
    VALUES(p_dava_id, p_avukat_id, p_aciklama, p_son_tarih, 'Bekliyor');
    SELECT LAST_INSERT_ID() AS yeni_id;
END $$

CREATE PROCEDURE sp_GorevGuncelle(
    IN p_id         INT,
    IN p_aciklama   VARCHAR(500),
    IN p_son_tarih  DATE,
    IN p_durum      VARCHAR(30)
)
BEGIN
    UPDATE gorevler
    SET aciklama=p_aciklama, son_tarih=p_son_tarih, durum=p_durum
    WHERE gorev_id = p_id;
END $$

CREATE PROCEDURE sp_GorevSil(IN p_id INT)
BEGIN
    DELETE FROM gorevler WHERE gorev_id = p_id;
END $$

CREATE PROCEDURE sp_GorevListele()
BEGIN
    SELECT g.gorev_id, g.aciklama, g.son_tarih, g.durum, g.olusturma_tarihi,
           d.dava_id, d.dava_no, d.dava_turu,
           CONCAT(a.ad,' ',a.soyad) AS avukat_adi,
           CONCAT(m.ad,' ',m.soyad) AS musteri_adi
    FROM gorevler g
    INNER JOIN davalar d ON g.dava_id = d.dava_id
    INNER JOIN avukatlar a ON g.avukat_id = a.avukat_id
    INNER JOIN musteriler m ON d.musteri_id = m.musteri_id
    ORDER BY g.son_tarih ASC;
END $$

CREATE PROCEDURE sp_DavaGorevleri(IN p_dava_id INT)
BEGIN
    SELECT g.gorev_id, g.aciklama, g.son_tarih, g.durum,
           CONCAT(a.ad,' ',a.soyad) AS avukat_adi
    FROM gorevler g
    INNER JOIN avukatlar a ON g.avukat_id = a.avukat_id
    WHERE g.dava_id = p_dava_id
    ORDER BY g.son_tarih ASC;
END $$

-- Dashboard istatistik
CREATE PROCEDURE sp_DashboardIstatistik()
BEGIN
    SELECT
        (SELECT COUNT(*) FROM musteriler)                           AS toplam_musteri,
        (SELECT COUNT(*) FROM davalar)                              AS toplam_dava,
        (SELECT COUNT(*) FROM davalar WHERE durum='Aktif')          AS aktif_dava,
        (SELECT COUNT(*) FROM durusmalar
         WHERE DATE(durusma_tarihi)=CURDATE())                      AS bugun_durusma,
        (SELECT COUNT(*) FROM gorevler
         WHERE durum IN ('Bekliyor','Devam Ediyor')
           AND son_tarih <= CURDATE())                              AS gecmis_gorev,
        (SELECT COALESCE(SUM(tutar),0) FROM odemeler
         WHERE MONTH(tarih)=MONTH(CURDATE())
           AND YEAR(tarih)=YEAR(CURDATE()))                         AS bu_ay_gelir;
END $$

DELIMITER ;

-- ============================================================
-- KULLANICI TANIMLI FONKSİYONLAR
-- ============================================================

DELIMITER $$

-- FUNCTION 1: Bir davaya ait toplam masrafı hesapla
CREATE FUNCTION fn_DavaMasrafToplam(p_dava_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE toplam DECIMAL(10,2);
    SELECT COALESCE(SUM(tutar), 0) INTO toplam
    FROM masraflar WHERE dava_id = p_dava_id;
    RETURN toplam;
END $$

-- FUNCTION 2: Müşterinin toplam ödediği tutarı hesapla
CREATE FUNCTION fn_MusteriOdemeToplam(p_musteri_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE toplam DECIMAL(10,2);
    SELECT COALESCE(SUM(tutar), 0) INTO toplam
    FROM odemeler WHERE musteri_id = p_musteri_id;
    RETURN toplam;
END $$

DELIMITER ;

-- ============================================================
-- TETİKLEYİCİLER (TRIGGERS)
-- ============================================================

DELIMITER $$

-- TRIGGER 1: Duruşma tamamlandığında dava durumunu kontrol et (AFTER UPDATE)
CREATE TRIGGER tg_durusma_sonuc_kaydet
AFTER UPDATE ON durusmalar
FOR EACH ROW
BEGIN
    -- Duruşma tamamlandığında, dava hâlâ aktifse devam et bilgisi loglanır
    IF NEW.durum = 'Tamamlandi' AND OLD.durum != 'Tamamlandi' THEN
        -- Son duruşma sonucunu dava açıklamasına ekle
        UPDATE davalar
        SET aciklama = CONCAT(
            IFNULL(aciklama,''), ' | Son durusma: ',
            DATE_FORMAT(NEW.durusma_tarihi,'%d.%m.%Y'),
            ' - ', IFNULL(NEW.sonuc,'Sonuc girilmedi')
        )
        WHERE dava_id = NEW.dava_id AND durum = 'Aktif';
    END IF;
END $$

-- TRIGGER 2: Görevin son tarihi geçmişse otomatik uyarı durumu ekle (BEFORE UPDATE)
CREATE TRIGGER tg_gorev_gecikme_kontrol
BEFORE UPDATE ON gorevler
FOR EACH ROW
BEGIN
    -- Tamamlanmamış görevi tekrar bekliyor yapılmak istenirse
    -- son tarihi geçmişse "Devam Ediyor" durumuna zorla
    IF NEW.durum = 'Bekliyor'
       AND NEW.son_tarih IS NOT NULL
       AND NEW.son_tarih < CURDATE() THEN
        SET NEW.durum = 'Devam Ediyor';
    END IF;
END $$

-- TRIGGER 3: Dava silindiğinde ilgili ödeme sayısını kaydet (BEFORE DELETE)
CREATE TRIGGER tg_dava_sil_kontrol
BEFORE DELETE ON davalar
FOR EACH ROW
BEGIN
    DECLARE odeme_sayisi INT;
    SELECT COUNT(*) INTO odeme_sayisi
    FROM odemeler WHERE dava_id = OLD.dava_id;
    -- Ödemesi olan dava silinemez
    IF odeme_sayisi > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bu davaya ait odeme kaydi var! Once odemeleri siliniz.';
    END IF;
END $$

DELIMITER ;

-- ============================================================
-- LEXTRACK — ÖRNEK VERİLER (Zenginleştirilmiş)
-- Bu scripti hukuk_burosu.sql'den SONRA çalıştırın
-- ============================================================

USE hukuk_burosu;



-- ============================================================
-- AVUKATLAR (8 avukat)
-- ============================================================
INSERT INTO avukatlar (ad, soyad, baro_no, uzmanlik, telefon, email, aktif) VALUES
('Ahmet',   'Yilmaz',  'BAR-2018-001', 'Ceza Hukuku',      '0532-101-1001', 'ahmet.yilmaz@lextrack.com',   1),
('Selin',   'Kara',    'BAR-2019-002', 'Is Hukuku',        '0532-101-1002', 'selin.kara@lextrack.com',     1),
('Emre',    'Demir',   'BAR-2017-003', 'Aile Hukuku',      '0532-101-1003', 'emre.demir@lextrack.com',     1),
('Burcu',   'Sahin',   'BAR-2020-004', 'Ticaret Hukuku',   '0532-101-1004', 'burcu.sahin@lextrack.com',    1),
('Murat',   'Celik',   'BAR-2016-005', 'Idare Hukuku',     '0532-101-1005', 'murat.celik@lextrack.com',    1),
('Ayse',    'Ozturk',  'BAR-2021-006', 'Icra Hukuku',      '0532-101-1006', 'ayse.ozturk@lextrack.com',    1),
('Kemal',   'Arslan',  'BAR-2015-007', 'Ceza Hukuku',      '0532-101-1007', 'kemal.arslan@lextrack.com',   1),
('Fatma',   'Bulut',   'BAR-2022-008', 'Genel Hukuk',      '0532-101-1008', 'fatma.bulut@lextrack.com',    0);

-- ============================================================
-- MÜŞTERİLER (18 müşteri)
-- ============================================================
INSERT INTO musteriler (ad, soyad, tc_no, telefon, email, adres) VALUES
('Mustafa',  'Ozturk',   '10000000001', '0555-201-0001', 'mustafa.ozturk@email.com',  'Bartin Merkez Mah. No:12'),
('Elif',     'Arslan',   '10000000002', '0555-201-0002', 'elif.arslan@email.com',     'Bartin Amasra Ilcesi'),
('Kerem',    'Bulut',    '10000000003', '0555-201-0003', 'kerem.bulut@email.com',     'Bartin Kozcagiz'),
('Zeynep',   'Celik',    '10000000004', '0555-201-0004', 'zeynep.celik@email.com',    'Bartin Ulus Ilcesi'),
('Haluk',    'Karadag',  '10000000005', '0555-201-0005', 'haluk.karadag@email.com',   'Bartin Merkez'),
('Neslihan', 'Yildirim', '10000000006', '0555-201-0006', 'neslihan@email.com',        'Bartin Inkumu'),
('Tarkan',   'Polat',    '10000000007', '0555-201-0007', 'tarkan.polat@email.com',    'Bartin Merkez Mah. No:45'),
('Sema',     'Gul',      '10000000008', '0555-201-0008', 'sema.gul@email.com',        'Bartin Hasankadı'),
('Cengiz',   'Akbas',    '10000000009', '0555-201-0009', 'cengiz.akbas@email.com',   'Bartin Merkez'),
('Derya',    'Koc',      '10000000010', '0555-201-0010', 'derya.koc@email.com',      'Bartin Kozcagiz'),
('Firat',    'Sen',      '10000000011', '0555-201-0011', 'firat.sen@email.com',       'Bartin Amasra'),
('Gamze',    'Tekin',    '10000000012', '0555-201-0012', 'gamze.tekin@email.com',     'Bartin Merkez Mah. No:78'),
('Ibrahim',  'Kurt',     '10000000013', '0555-201-0013', 'ibrahim.kurt@email.com',    'Bartin Ulus'),
('Jale',     'Tas',      '10000000014', '0555-201-0014', 'jale.tas@email.com',        'Bartin Merkez'),
('Koray',    'Erdem',    '10000000015', '0555-201-0015', 'koray.erdem@email.com',     'Bartin Inkumu Mah.'),
('Lale',     'Simsek',   '10000000016', '0555-201-0016', 'lale.simsek@email.com',     'Bartin Merkez'),
('Mehmet',   'Dogan',    '10000000017', '0555-201-0017', 'mehmet.dogan@email.com',    'Bartin Kozcagiz Ilcesi'),
('Nazli',    'Acar',     '10000000018', '0555-201-0018', 'nazli.acar@email.com',      'Bartin Amasra Sahil');

-- ============================================================
-- DAVALAR (22 dava)
-- ============================================================
INSERT INTO davalar (musteri_id, avukat_id, dava_no, dava_turu, mahkeme, acilis_tarihi, durum, aciklama) VALUES
(1,  1, '2024/1001', 'Ceza Davasi',          'Bartin 2. Agir Ceza Mahkemesi',   '2024-03-10', 'Kazanildi',   'Hirsizlik suclamas. Beraat karari verildi.'),
(2,  2, '2024/1002', 'Is Davasi',            'Bartin Is Mahkemesi',             '2024-04-15', 'Kazanildi',   'Haksiz isten cikarma. Tazminat odendi.'),
(3,  3, '2024/1003', 'Bosanma Davasi',       'Bartin Aile Mahkemesi',           '2024-05-20', 'Uzlasma',     'Anlasmal bosanma tamamlandi.'),
(4,  4, '2024/1004', 'Ticari Anlasmazlik',   'Bartin Ticaret Mahkemesi',        '2024-06-01', 'Kazanildi',   'Sozlesme ihlali. Alacak tahsil edildi.'),
(5,  1, '2024/1005', 'Ceza Davasi',          'Bartin 1. Agir Ceza Mahkemesi',   '2024-07-12', 'Kaybedildi',  'Dolandiricilik suclamas. Mahkumiyet.'),
(6,  5, '2024/1006', 'Idare Davasi',         'Bartin Idare Mahkemesi',          '2024-08-03', 'Kazanildi',   'Haksiz ihrac iptal edildi.'),
(7,  2, '2024/1007', 'Is Davasi',            'Bartin Is Mahkemesi',             '2024-09-18', 'Uzlasma',     'Kidem tazminati anlasmayla odendi.'),
(8,  6, '2024/1008', 'Icra Takibi',          'Bartin Icra Hukuk Mahkemesi',     '2024-10-05', 'Kazanildi',   'Alacak icra yoluyla tahsil edildi.'),
(9,  3, '2024/1009', 'Miras Davasi',         'Bartin Sulh Hukuk Mahkemesi',     '2024-11-22', 'Aktif',       'Miras paylasimi anlasmazi devam ediyor.'),
(10, 4, '2024/1010', 'Tazminat Davasi',      'Bartin 1. Asliye Hukuk',          '2024-12-10', 'Aktif',       'Trafik kazasi tazminat talebi.'),
(11, 7, '2025/1011', 'Ceza Davasi',          'Bartin 2. Agir Ceza Mahkemesi',   '2025-01-08', 'Aktif',       'Tehdit ve hakaret suclamas.'),
(12, 1, '2025/1012', 'Bosanma Davasi',       'Bartin Aile Mahkemesi',           '2025-02-14', 'Aktif',       'Cekismeli bosanma. Velayet talebi var.'),
(13, 5, '2025/1013', 'Idare Davasi',         'Bartin Idare Mahkemesi',          '2025-03-01', 'Aktif',       'Ruhsat iptali kararina itiraz.'),
(14, 2, '2025/1014', 'Is Davasi',            'Bartin Is Mahkemesi',             '2025-03-25', 'Aktif',       'Mobbing ve is guvencesi ihlali.'),
(15, 6, '2025/1015', 'Icra Takibi',          'Bartin Icra Hukuk Mahkemesi',     '2025-04-10', 'Aktif',       'Senet alacagi icra takibi.'),
(16, 3, '2025/1016', 'Miras Davasi',         'Bartin Sulh Hukuk Mahkemesi',     '2025-04-20', 'Aktif',       'Vasiyetname iptali talebi.'),
(17, 4, '2025/1017', 'Ticari Anlasmazlik',   'Bartin Ticaret Mahkemesi',        '2025-05-05', 'Aktif',       'Ortaklik anlasmazligi.'),
(18, 7, '2025/1018', 'Tazminat Davasi',      'Bartin 2. Asliye Hukuk',          '2025-05-15', 'Aktif',       'Tibbi ihmal tazminat davasi.'),
(1,  1, '2026/1019', 'Ceza Davasi',          'Bartin 1. Agir Ceza Mahkemesi',   '2026-01-10', 'Aktif',       'Yeni ceza davasi basladi.'),
(5,  2, '2026/1020', 'Is Davasi',            'Bartin Is Mahkemesi',             '2026-02-20', 'Aktif',       'Ucret alacagi talebi.'),
(9,  5, '2026/1021', 'Idare Davasi',         'Bartin Idare Mahkemesi',          '2026-03-15', 'Aktif',       'Vergi cezasina itiraz.'),
(12, 3, '2026/1022', 'Bosanma Davasi',       'Bartin Aile Mahkemesi',           '2026-04-01', 'Aktif',       'Nafaka ve mal paylasimi talebi.');

-- ============================================================
-- DURUŞMALAR (30 duruşma)
-- ============================================================
INSERT INTO durusmalar (dava_id, durusma_tarihi, sonuc, notlar, durum) VALUES
-- Tamamlanmış davalar
(1,  '2024-05-10 09:30:00', 'Taniklar dinlendi',            'Savunma avukati itirazlari sundu',          'Tamamlandi'),
(1,  '2024-07-22 10:00:00', 'Bilirkisi raporu incelendi',   'Mahkeme bilirkisi atadi',                   'Tamamlandi'),
(1,  '2024-09-15 09:00:00', 'Beraat karari verildi',        'Musteri beraat etti. Dava kapandi.',         'Tamamlandi'),
(2,  '2024-06-18 14:00:00', 'Islak imza tutanagi alindi',   'Isci taraf delillerini sundu',              'Tamamlandi'),
(2,  '2024-08-30 11:00:00', 'Uzlasma sagland',              'Taraflar anlasti. Tazminat belirlendi.',     'Tamamlandi'),
(3,  '2024-07-05 10:30:00', 'Mal paylasimi gorusmesi',      'Taraflar uzlasma yoluna gitti',             'Tamamlandi'),
(4,  '2024-08-12 09:30:00', 'Sozlesme belgesi incelendi',   'Uzman gorusu istendi',                      'Tamamlandi'),
(4,  '2024-10-20 10:00:00', 'Karar aciklandi',              'Alacak lehine karar cikti',                 'Tamamlandi'),
(5,  '2024-09-05 09:00:00', 'Tanik ifadesi alindi',         'Aleyhe tanik beyani',                       'Tamamlandi'),
(5,  '2024-11-14 10:30:00', 'Karar aciklandi',              'Mahkumiyet karari verildi. Temyize gidilecek.','Tamamlandi'),
-- Aktif davalar
(9,  '2024-12-15 09:30:00', 'Taraflar dinlendi',            'Her iki taraf da beyanda bulundu',          'Tamamlandi'),
(9,  '2025-02-20 10:00:00', 'Bilirkisi tayin edildi',       'Miras taksimat bilirkisisi atandi',         'Tamamlandi'),
(9,  '2026-07-10 09:00:00', NULL,                           'Bilirkisi raporu bekleniyor',               'Planlandi'),
(10, '2025-01-08 11:00:00', 'Kaza tespit tutanagi incelendi','Sigorta sirketinden bilgi istendi',        'Tamamlandi'),
(10, '2025-04-15 09:30:00', 'Bilirkisi raporu sunuldu',     'Hasar tespit raporu mahkemeye sunuldu',     'Tamamlandi'),
(10, '2026-06-20 10:00:00', NULL,                           'Karar durusmasi',                           'Planlandi'),
(11, '2025-03-10 09:00:00', 'Sikayet eden taraf dinlendi',  'Mesaj kayitlari delil olarak sunuldu',      'Tamamlandi'),
(11, '2025-05-22 10:30:00', 'Sanik ifadesi alindi',         'Savunma hazirlanacak',                      'Tamamlandi'),
(11, '2026-06-05 09:30:00', NULL,                           'Uzman tanik dinlenecek',                    'Planlandi'),
(12, '2025-04-08 11:00:00', 'Taraflar dinlendi',            'Her iki taraf avukatli. Cekismeli gidiyor.','Tamamlandi'),
(12, '2025-06-18 09:00:00', 'Cocuk velayeti uzmani raporu','Uzman raporu mahkemeye teslim edildi',       'Tamamlandi'),
(12, '2026-05-15 10:00:00', NULL,                           'Velayet karari bekleniyor',                 'Ertelendi'),
(12, '2026-07-22 09:30:00', NULL,                           'Yeniden planland',                         'Planlandi'),
(14, '2025-05-12 14:00:00', 'Isci taraf taniklarini sundu', 'Iscinin yazismalari incelendi',             'Tamamlandi'),
(14, '2025-08-20 10:00:00', 'Isveren taraf dinlendi',       'Isverenin savunmasi alindi',                'Tamamlandi'),
(14, '2026-06-10 09:00:00', NULL,                           'Bilirkisi raporu bekleniyor',               'Planlandi'),
(19, '2026-02-15 09:30:00', 'Ilk durusma yapildi',          'Taraflar tanitildi',                        'Tamamlandi'),
(19, '2026-04-20 10:00:00', 'Deliller sunuldu',             'MOBESE kayitlari mahkemeye verildi',        'Tamamlandi'),
(19, '2026-06-01 10:00:00', 'Tanik dinlendi',               'Gorgul tanik ifadesi alindi',               'Tamamlandi'),
(20, '2026-03-18 11:00:00', 'Ilk durusma',                  'Ucret alacagi hesap dökümü istendi',        'Tamamlandi'),
(20, '2026-05-25 09:30:00', NULL,                           'Muhasebe uzmani dinlenecek',                'Planlandi');

-- ============================================================
-- BELGELER (25+ belge)
-- ============================================================
INSERT INTO belgeler (dava_id, belge_adi, belge_turu, aciklama) VALUES
(1,  'Iddianame_2024_1001.pdf',       'Iddianame',  'Savci tarafindan hazirlanan iddianame'),
(1,  'Tanik_Ifadesi_Ahmet.docx',      'Ifade',      'Gorgul tanik Ahmet Beyin ifadesi'),
(1,  'MOBESE_Kaydi_Analizi.pdf',      'Rapor',      'Kamera kaydi analiz raporu'),
(1,  'Beraat_Karari.pdf',             'Karar',      'Mahkeme beraat karari'),
(2,  'Is_Sozlesmesi.pdf',             'Sozlesme',   'Asil is sozlesmesi'),
(2,  'Fesih_Bildirimi.pdf',           'Belge',      'Isveren fesih bildirimi'),
(2,  'SGK_Kayitlari.pdf',             'Rapor',      'SGK istihdak kayitlari'),
(2,  'Uzlasma_Tutanagi.pdf',          'Tutanak',    'Taraflarin imzalad uzlasma belgesi'),
(3,  'Bosanma_Dilekce.docx',          'Dilekce',    'Bosanma davasi acilis dileksesi'),
(3,  'Mal_Varligi_Listesi.xlsx',      'Belge',      'Ortak mal varligi dokumu'),
(3,  'Protokol_Final.pdf',            'Protokol',   'Imzali bosanma protokolu'),
(4,  'Ticari_Sozlesme.pdf',           'Sozlesme',   'Taraflar arasi ticari sozlesme'),
(4,  'Fatura_Kayitlari.pdf',          'Belge',      'Odenmemis fatura kayitlari'),
(4,  'Bilirkisi_Raporu.pdf',          'Rapor',      'Ticaret mahkemesi bilirkisi raporu'),
(9,  'Vasiyetname.pdf',               'Vasiyetname','Miras birakana ait vasiyetname'),
(9,  'Tapu_Kayitlari.pdf',            'Tapu',       'Miras konusu tasinmaz kayitlari'),
(10, 'Kaza_Tutanagi.pdf',             'Tutanak',    'Trafik kaza tespit tutanagi'),
(10, 'Sigorta_Policesi.pdf',          'Sozlesme',   'Arac kasko sigortasi'),
(10, 'Hasar_Bilirkisi.pdf',           'Rapor',      'Arac hasar tespit raporu'),
(11, 'Sikayet_Dilekce.docx',          'Dilekce',    'Savciliğa verilen sikayet dileksesi'),
(11, 'Whatsapp_Ekran_Goruntuleri.pdf','Delil',      'Tehdit iceren mesaj ekran goruntuleri'),
(12, 'Bosanma_Dilekce.docx',          'Dilekce',    'Cekismeli bosanma basvuru dileksesi'),
(12, 'Velayet_Uzman_Raporu.pdf',      'Rapor',      'Cocuk psikoloji uzman degerlendirmesi'),
(14, 'Is_Sozlesmesi_2023.pdf',        'Sozlesme',   'Asil is sozlesmesi'),
(14, 'Mobbing_Delilleri.pdf',         'Delil',      'Mobbing iddiasina iliskin yazismalar'),
(19, 'Iddianame_2026.pdf',            'Iddianame',  'Yeni dava iddianamesi'),
(20, 'Ucret_Bordrolari.pdf',          'Belge',      'Son 12 aylik maas bordrolari');

-- ============================================================
-- MASRAFLAR (25+ masraf)
-- ============================================================
INSERT INTO masraflar (dava_id, aciklama, tutar, tarih, tur) VALUES
(1,  'Dava acma harci',           350.00,  '2024-03-10', 'Mahkeme Harci'),
(1,  'Bilirkisi ucreti',         1500.00,  '2024-07-22', 'Bilirkisi'),
(1,  'Tercume ucreti',            400.00,  '2024-05-15', 'Tercume'),
(1,  'Posta ve tebligat',          85.00,  '2024-04-01', 'Diger'),
(2,  'Dava acma harci',           280.00,  '2024-04-15', 'Mahkeme Harci'),
(2,  'SGK kayit ucreti',          150.00,  '2024-06-01', 'Diger'),
(2,  'Avukatlik ucreti',         5000.00,  '2024-04-15', 'Avukatlik Ucreti'),
(3,  'Bosanma harci',             500.00,  '2024-05-20', 'Mahkeme Harci'),
(3,  'Noter ucreti',              650.00,  '2024-06-10', 'Diger'),
(4,  'Dava harci',                450.00,  '2024-06-01', 'Mahkeme Harci'),
(4,  'Bilirkisi ucreti',         2000.00,  '2024-09-01', 'Bilirkisi'),
(4,  'Avukatlik ucreti',         8000.00,  '2024-06-01', 'Avukatlik Ucreti'),
(5,  'Ceza davasi harci',         200.00,  '2024-07-12', 'Mahkeme Harci'),
(5,  'Tanik masrafi',             300.00,  '2024-09-05', 'Diger'),
(9,  'Dava harci',                380.00,  '2024-11-22', 'Mahkeme Harci'),
(9,  'Bilirkisi ucreti',         2500.00,  '2025-03-01', 'Bilirkisi'),
(9,  'Tapu arastirma ucreti',     200.00,  '2024-12-10', 'Diger'),
(10, 'Dava harci',                420.00,  '2024-12-10', 'Mahkeme Harci'),
(10, 'Hasar bilirkisi',          1800.00,  '2025-02-15', 'Bilirkisi'),
(10, 'Kaza yeri kesif',           600.00,  '2025-01-20', 'Diger'),
(11, 'Ceza harci',                180.00,  '2025-01-08', 'Mahkeme Harci'),
(12, 'Bosanma harci',             550.00,  '2025-02-14', 'Mahkeme Harci'),
(12, 'Uzman ucret',              1200.00,  '2025-07-01', 'Bilirkisi'),
(14, 'Is mahkemesi harci',        320.00,  '2025-03-25', 'Mahkeme Harci'),
(14, 'Avukatlik ucreti',         6000.00,  '2025-03-25', 'Avukatlik Ucreti'),
(19, 'Dava harci',                250.00,  '2026-01-10', 'Mahkeme Harci'),
(20, 'Is harci',                  300.00,  '2026-02-20', 'Mahkeme Harci');

-- ============================================================
-- ÖDEMELER (20+ ödeme)
-- ============================================================
INSERT INTO odemeler (musteri_id, dava_id, tutar, tarih, tur, aciklama) VALUES
(1,  1,  3000.00,  '2024-03-15 10:00:00', 'Nakit',            'Avukatlik ucreti pesin'),
(1,  1,  2000.00,  '2024-07-01 11:00:00', 'Banka Transferi',  'Dava giderleri 2. odeme'),
(2,  2,  5000.00,  '2024-04-20 09:30:00', 'Kredi Karti',      'Avukatlik ucreti'),
(2,  2,  1500.00,  '2024-08-05 14:00:00', 'Nakit',            'Ek giderler'),
(3,  3,  4000.00,  '2024-05-25 10:00:00', 'Banka Transferi',  'Bosanma davasi ucreti'),
(4,  4,  8000.00,  '2024-06-10 09:00:00', 'Kredi Karti',      'Ticaret davasi avukatlik'),
(4,  4,  3000.00,  '2024-10-25 11:00:00', 'Nakit',            'Ek masraflar'),
(5,  5,  3500.00,  '2024-07-20 10:30:00', 'Banka Transferi',  'Ceza davasi ucreti'),
(6,  6,  4500.00,  '2024-08-10 09:00:00', 'Nakit',            'Idare davasi avukatlik'),
(7,  7,  2500.00,  '2024-09-25 11:00:00', 'Kredi Karti',      'Is davasi uzlasma ucreti'),
(8,  8,  3200.00,  '2024-10-12 10:00:00', 'Banka Transferi',  'Icra takibi'),
(9,  9,  2000.00,  '2024-12-01 09:30:00', 'Nakit',            'Miras davasi pesin'),
(9,  9,  2000.00,  '2025-04-15 10:00:00', 'Banka Transferi',  'Miras davasi 2. taksit'),
(10, 10, 1500.00,  '2025-01-15 11:00:00', 'Nakit',            'Tazminat davasi baslangic'),
(10, 10, 2000.00,  '2025-05-20 09:00:00', 'Kredi Karti',      'Tazminat 2. odeme'),
(11, 11, 2500.00,  '2025-01-20 10:30:00', 'Nakit',            'Ceza davasi pesin'),
(12, 12, 3000.00,  '2025-02-20 09:00:00', 'Banka Transferi',  'Bosanma davasi baslangic'),
(12, 12, 2000.00,  '2025-08-10 11:00:00', 'Nakit',            'Devam odemesi'),
(14, 14, 6000.00,  '2025-04-05 10:00:00', 'Kredi Karti',      'Is davasi avukatlik ucreti'),
(1,  19, 2000.00,  '2026-01-20 09:30:00', 'Nakit',            'Yeni ceza davasi pesin'),
(5,  20, 3000.00,  '2026-03-01 10:00:00', 'Banka Transferi',  'Is davasi avukatlik');

-- ============================================================
-- GÖREVLER (20+ görev)
-- ============================================================
INSERT INTO gorevler (dava_id, avukat_id, aciklama, son_tarih, durum) VALUES
-- Tamamlanmış görevler
(1,  1, 'Beraat karari kesinlestirme belgesi al',       '2024-10-01', 'Tamamlandi'),
(2,  2, 'Tazminat odeme belgelerini dosyala',           '2024-09-15', 'Tamamlandi'),
(3,  3, 'Bosanma kararini nufusa isle',                 '2024-08-20', 'Tamamlandi'),
(4,  4, 'Alacak tahsil belgelerini muhafaza et',        '2024-11-30', 'Tamamlandi'),
(9,  3, 'Tapu devir islemleri icin gerekli belgeler',   '2025-01-15', 'Tamamlandi'),
(9,  3, 'Bilirkisi ile gorusme planla',                 '2025-02-28', 'Tamamlandi'),
-- Devam eden görevler
(10, 4, 'Sigorta sirketinden hasar raporu talep et',    '2026-06-10', 'Tamamlandi'),
(10, 4, 'Karar oncesi ozet dilekce hazirla',            '2026-06-15', 'Devam Ediyor'),
(11, 7, 'Uzman tanik listesi hazirla',                  '2026-05-30', 'Tamamlandi'),
(11, 7, 'Savunma dilekce taslagi olustur',              '2026-06-08', 'Devam Ediyor'),
(12, 3, 'Velayet uzman raporunu mahkemeye sun',         '2026-06-01', 'Tamamlandi'),
(12, 3, 'Yeni durusma hazirlik dosyasi',                '2026-07-15', 'Devam Ediyor'),
(14, 2, 'Bilirkisi raporunu incele ve itiraz yaz',      '2026-06-15', 'Devam Ediyor'),
(14, 2, 'Isci lehine emsal kararlari topla',            '2026-06-20', 'Bekliyor'),
(17, 4, 'Ortaklik anlasmazligi icin finansal analiz',   '2026-06-25', 'Bekliyor'),
(18, 7, 'Tibbi kayitlari ve raporlari topla',           '2026-06-30', 'Devam Ediyor'),
(19, 1, 'MOBESE kaydi analizi raporunu hazirla',        '2026-06-05', 'Tamamlandi'),
(19, 1, 'Bir sonraki durusma savunma dosyasi',          '2026-06-25', 'Devam Ediyor'),
(20, 2, 'Muhasebe uzmanindan rapor al',                 '2026-05-28', 'Devam Ediyor'),
(20, 2, 'Bordro analizi ozeti hazirla',                 '2026-06-10', 'Bekliyor'),
(21, 5, 'Vergi cezasi itiraz dilekce taslagi',          '2026-06-20', 'Bekliyor'),
(22, 3, 'Nafaka hesap tablolari hazirla',               '2026-07-01', 'Bekliyor');

-- Özet kontrol
SELECT 'Avukatlar'  AS Tablo, COUNT(*) AS Adet FROM avukatlar  UNION ALL
SELECT 'Musteriler',          COUNT(*)          FROM musteriler UNION ALL
SELECT 'Davalar',             COUNT(*)          FROM davalar    UNION ALL
SELECT 'Durusmalar',          COUNT(*)          FROM durusmalar UNION ALL
SELECT 'Belgeler',            COUNT(*)          FROM belgeler   UNION ALL
SELECT 'Masraflar',           COUNT(*)          FROM masraflar  UNION ALL
SELECT 'Odemeler',            COUNT(*)          FROM odemeler   UNION ALL
SELECT 'Gorevler',            COUNT(*)          FROM gorevler;

-- ============================================================
-- VIEW'LER
-- ============================================================

CREATE OR REPLACE VIEW view_aktif_davalar AS
SELECT
    d.dava_id, d.dava_no, d.dava_turu, d.mahkeme,
    d.acilis_tarihi, d.durum,
    CONCAT(m.ad,' ',m.soyad) AS musteri_adi,
    m.telefon                AS musteri_tel,
    CONCAT(a.ad,' ',a.soyad) AS avukat_adi,
    a.uzmanlik               AS avukat_uzmanlik
FROM davalar d
INNER JOIN musteriler m ON d.musteri_id = m.musteri_id
INNER JOIN avukatlar  a ON d.avukat_id  = a.avukat_id
WHERE d.durum = 'Aktif';

CREATE OR REPLACE VIEW view_musteri_mali_ozet AS
SELECT
    m.musteri_id,
    CONCAT(m.ad,' ',m.soyad)      AS musteri_adi,
    m.telefon,
    COUNT(DISTINCT d.dava_id)     AS toplam_dava,
    COALESCE(SUM(o.tutar),0)      AS toplam_odeme,
    COALESCE(SUM(ms.tutar),0)     AS toplam_masraf
FROM musteriler m
LEFT JOIN davalar   d  ON m.musteri_id = d.musteri_id
LEFT JOIN odemeler  o  ON d.dava_id    = o.dava_id
LEFT JOIN masraflar ms ON d.dava_id    = ms.dava_id
GROUP BY m.musteri_id, m.ad, m.soyad, m.telefon;

CREATE OR REPLACE VIEW view_yaklasan_durusmalar AS
SELECT
    dr.durusma_id, dr.durusma_tarihi, dr.durum,
    d.dava_no, d.dava_turu, d.mahkeme,
    CONCAT(m.ad,' ',m.soyad) AS musteri_adi,
    CONCAT(a.ad,' ',a.soyad) AS avukat_adi
FROM durusmalar dr
INNER JOIN davalar    d ON dr.dava_id   = d.dava_id
INNER JOIN musteriler m ON d.musteri_id = m.musteri_id
INNER JOIN avukatlar  a ON d.avukat_id  = a.avukat_id
WHERE dr.durum = 'Planlandi'
  AND dr.durusma_tarihi BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
ORDER BY dr.durusma_tarihi ASC;

-- ============================================================
-- TRANSACTION STORED PROCEDURE'LERİ
-- ============================================================

DELIMITER $$

CREATE PROCEDURE sp_DavaKapat(
    IN p_dava_id    INT,
    IN p_yeni_durum VARCHAR(30),
    IN p_avukat_id  INT)
BEGIN
    DECLARE v_hata INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_hata = 1;

    START TRANSACTION;

    UPDATE davalar
    SET durum = p_yeni_durum
    WHERE dava_id = p_dava_id;

    UPDATE gorevler
    SET durum = 'Iptal'
    WHERE dava_id = p_dava_id
      AND durum IN ('Bekliyor', 'Devam Ediyor');

    INSERT INTO gorevler(dava_id, avukat_id, aciklama, son_tarih, durum)
    VALUES(p_dava_id, p_avukat_id,
        CONCAT('Dava kapanisi: ', p_yeni_durum, ' - Dosyalama yapilacak'),
        DATE_ADD(CURDATE(), INTERVAL 7 DAY), 'Bekliyor');

    IF v_hata = 0 THEN
        COMMIT;
        SELECT 'BASARILI' AS sonuc, 'Dava basariyla kapatildi.' AS mesaj;
    ELSE
        ROLLBACK;
        SELECT 'HATA' AS sonuc, 'Islem geri alindi.' AS mesaj;
    END IF;
END $$

CREATE PROCEDURE sp_MusteriVeDavaEkle(
    IN p_ad             VARCHAR(64),
    IN p_soyad          VARCHAR(64),
    IN p_tc_no          VARCHAR(11),
    IN p_telefon        VARCHAR(20),
    IN p_email          VARCHAR(100),
    IN p_adres          VARCHAR(250),
    IN p_avukat_id      INT,
    IN p_dava_no        VARCHAR(50),
    IN p_dava_turu      VARCHAR(100),
    IN p_mahkeme        VARCHAR(200))
BEGIN
    DECLARE v_hata       INT DEFAULT 0;
    DECLARE v_musteri_id INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_hata = 1;

    START TRANSACTION;

    INSERT INTO musteriler(ad, soyad, tc_no, telefon, email, adres)
    VALUES(p_ad, p_soyad, p_tc_no, p_telefon, p_email, p_adres);

    SET v_musteri_id = LAST_INSERT_ID();

    INSERT INTO davalar(musteri_id, avukat_id, dava_no, dava_turu, mahkeme, durum)
    VALUES(v_musteri_id, p_avukat_id, p_dava_no, p_dava_turu, p_mahkeme, 'Aktif');

    IF v_hata = 0 THEN
        COMMIT;
        SELECT 'BASARILI' AS sonuc, v_musteri_id AS musteri_id, LAST_INSERT_ID() AS dava_id;
    ELSE
        ROLLBACK;
        SELECT 'HATA' AS sonuc, 'Islem geri alindi.' AS mesaj;
    END IF;
END $$

DELIMITER ;
