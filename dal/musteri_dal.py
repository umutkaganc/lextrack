from dal.db import call_proc, call_proc_void

def listele():          return call_proc('sp_MusteriListele')
def getir(id):
    r = call_proc('sp_MusteriGetir', (id,)); return r[0] if r else None
def ekle(ad,soyad,tc_no,telefon,email,adres):
    r = call_proc('sp_MusteriEkle', (ad,soyad,tc_no,telefon,email,adres))
    return r[0]['yeni_id'] if r else None
def guncelle(id,ad,soyad,tc_no,telefon,email,adres):
    call_proc_void('sp_MusteriGuncelle', (id,ad,soyad,tc_no,telefon,email,adres))
def sil(id):            call_proc_void('sp_MusteriSil', (id,))
