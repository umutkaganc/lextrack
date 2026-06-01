# bll/services.py — İş Katmanı
# Doğrulama ve iş kuralları burada. SQL kodu YOKTUR.

from dal import (avukat_dal, musteri_dal, dava_dal, durusma_dal,
                 belge_dal, masraf_dal, odeme_dal, gorev_dal, dashboard_dal)


def dashboard_istatistik():     return dashboard_dal.istatistik()

# ── AVUKATLAR ──────────────────────────────────────────────
def avukat_listele():           return avukat_dal.listele()
def avukat_getir(id):           return avukat_dal.getir(id)

def avukat_ekle(f):
    ad=f.get('ad','').strip(); soyad=f.get('soyad','').strip()
    baro_no=f.get('baro_no','').strip(); uzmanlik=f.get('uzmanlik','').strip()
    telefon=f.get('telefon','').strip(); email=f.get('email','').strip()
    if not ad or not soyad or not baro_no:
        raise ValueError('Ad, soyad ve baro no zorunludur.')
    return avukat_dal.ekle(ad, soyad, baro_no, uzmanlik, telefon, email)

def avukat_guncelle(id, f):
    ad=f.get('ad','').strip(); soyad=f.get('soyad','').strip()
    baro_no=f.get('baro_no','').strip(); uzmanlik=f.get('uzmanlik','').strip()
    telefon=f.get('telefon','').strip(); email=f.get('email','').strip()
    aktif=1 if f.get('aktif') else 0
    avukat_dal.guncelle(id, ad, soyad, baro_no, uzmanlik, telefon, email, aktif)

def avukat_sil(id):             avukat_dal.sil(id)

# ── MÜŞTERİLER ─────────────────────────────────────────────
def musteri_listele():          return musteri_dal.listele()
def musteri_getir(id):          return musteri_dal.getir(id)

def musteri_ekle(f):
    ad=f.get('ad','').strip(); soyad=f.get('soyad','').strip()
    tc_no=f.get('tc_no','').strip(); telefon=f.get('telefon','').strip()
    email=f.get('email','').strip(); adres=f.get('adres','').strip()
    if not ad or not soyad or not tc_no:
        raise ValueError('Ad, soyad ve TC No zorunludur.')
    if len(tc_no) != 11 or not tc_no.isdigit():
        raise ValueError('TC No 11 haneli rakam olmalıdır.')
    return musteri_dal.ekle(ad, soyad, tc_no, telefon, email, adres)

def musteri_guncelle(id, f):
    ad=f.get('ad','').strip(); soyad=f.get('soyad','').strip()
    tc_no=f.get('tc_no','').strip(); telefon=f.get('telefon','').strip()
    email=f.get('email','').strip(); adres=f.get('adres','').strip()
    musteri_dal.guncelle(id, ad, soyad, tc_no, telefon, email, adres)

def musteri_sil(id):            musteri_dal.sil(id)

# ── DAVALAR ────────────────────────────────────────────────
def dava_listele():             return dava_dal.listele()
def dava_getir(id):             return dava_dal.getir(id)

def dava_ekle(f):
    musteri_id=f.get('musteri_id'); avukat_id=f.get('avukat_id')
    dava_no=f.get('dava_no','').strip(); dava_turu=f.get('dava_turu','').strip()
    mahkeme=f.get('mahkeme','').strip()
    acilis_tarihi=f.get('acilis_tarihi') or None
    aciklama=f.get('aciklama','').strip()
    if not musteri_id or not avukat_id or not dava_no:
        raise ValueError('Müşteri, avukat ve dava no zorunludur.')
    return dava_dal.ekle(musteri_id, avukat_id, dava_no, dava_turu, mahkeme, acilis_tarihi, aciklama)

def dava_guncelle(id, f):
    musteri_id=f.get('musteri_id'); avukat_id=f.get('avukat_id')
    dava_no=f.get('dava_no','').strip(); dava_turu=f.get('dava_turu','').strip()
    mahkeme=f.get('mahkeme','').strip(); durum=f.get('durum','Aktif')
    aciklama=f.get('aciklama','').strip()
    dava_dal.guncelle(id, musteri_id, avukat_id, dava_no, dava_turu, mahkeme, durum, aciklama)

def dava_sil(id):               dava_dal.sil(id)

# ── DURUŞMALAR ─────────────────────────────────────────────
def durusma_listele():          return durusma_dal.listele()
def dava_durusmalari(dava_id):  return durusma_dal.dava_durusmalari(dava_id)

def durusma_ekle(f):
    dava_id=f.get('dava_id'); tarih=f.get('durusma_tarihi'); notlar=f.get('notlar','').strip()
    if not dava_id or not tarih:
        raise ValueError('Dava ve tarih zorunludur.')
    return durusma_dal.ekle(dava_id, tarih, notlar)

def durusma_guncelle(id, f):
    tarih=f.get('durusma_tarihi'); sonuc=f.get('sonuc','').strip()
    notlar=f.get('notlar','').strip(); durum=f.get('durum','Planlandi')
    durusma_dal.guncelle(id, tarih, sonuc, notlar, durum)

def durusma_sil(id):            durusma_dal.sil(id)

# ── BELGELER ───────────────────────────────────────────────
def dava_belgeleri(dava_id):    return belge_dal.dava_belgeleri(dava_id)

def belge_ekle(f):
    dava_id=f.get('dava_id'); belge_adi=f.get('belge_adi','').strip()
    belge_turu=f.get('belge_turu','Diger'); aciklama=f.get('aciklama','').strip()
    if not dava_id or not belge_adi:
        raise ValueError('Dava ve belge adı zorunludur.')
    return belge_dal.ekle(dava_id, belge_adi, belge_turu, aciklama)

def belge_sil(id):              belge_dal.sil(id)

# ── MASRAFLAR ──────────────────────────────────────────────
def dava_masraflari(dava_id):   return masraf_dal.dava_masraflari(dava_id)

def masraf_ekle(f):
    dava_id=f.get('dava_id'); aciklama=f.get('aciklama','').strip()
    tutar=float(f.get('tutar',0)); tarih=f.get('tarih') or None
    tur=f.get('tur','Diger')
    if not dava_id or not aciklama:
        raise ValueError('Dava ve açıklama zorunludur.')
    return masraf_dal.ekle(dava_id, aciklama, tutar, tarih, tur)

def masraf_sil(id):             masraf_dal.sil(id)

# ── ÖDEMELER ───────────────────────────────────────────────
def odeme_listele():            return odeme_dal.listele()
def dava_odemeleri(dava_id):    return odeme_dal.dava_odemeleri(dava_id)

def odeme_ekle(f):
    musteri_id=f.get('musteri_id'); dava_id=f.get('dava_id')
    tutar=float(f.get('tutar',0)); tur=f.get('tur','Nakit')
    aciklama=f.get('aciklama','').strip()
    if not musteri_id or not dava_id or tutar <= 0:
        raise ValueError('Müşteri, dava ve geçerli tutar zorunludur.')
    return odeme_dal.ekle(musteri_id, dava_id, tutar, tur, aciklama)

def odeme_sil(id):              odeme_dal.sil(id)

# ── GÖREVLER ───────────────────────────────────────────────
def gorev_listele():            return gorev_dal.listele()
def dava_gorevleri(dava_id):    return gorev_dal.dava_gorevleri(dava_id)

def gorev_ekle(f):
    dava_id=f.get('dava_id'); avukat_id=f.get('avukat_id')
    aciklama=f.get('aciklama','').strip(); son_tarih=f.get('son_tarih') or None
    if not dava_id or not avukat_id or not aciklama:
        raise ValueError('Dava, avukat ve açıklama zorunludur.')
    return gorev_dal.ekle(dava_id, avukat_id, aciklama, son_tarih)

def gorev_guncelle(id, f):
    aciklama=f.get('aciklama','').strip(); son_tarih=f.get('son_tarih') or None
    durum=f.get('durum','Bekliyor')
    gorev_dal.guncelle(id, aciklama, son_tarih, durum)

def gorev_sil(id):              gorev_dal.sil(id)
