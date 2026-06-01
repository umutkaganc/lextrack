from dal.db import call_proc, call_proc_void

def listele():          return call_proc('sp_AvukatListele')
def getir(id):
    r = call_proc('sp_AvukatGetir', (id,)); return r[0] if r else None
def ekle(ad,soyad,baro_no,uzmanlik,telefon,email):
    r = call_proc('sp_AvukatEkle', (ad,soyad,baro_no,uzmanlik,telefon,email))
    return r[0]['yeni_id'] if r else None
def guncelle(id,ad,soyad,baro_no,uzmanlik,telefon,email,aktif):
    call_proc_void('sp_AvukatGuncelle', (id,ad,soyad,baro_no,uzmanlik,telefon,email,aktif))
def sil(id):            call_proc_void('sp_AvukatSil', (id,))
