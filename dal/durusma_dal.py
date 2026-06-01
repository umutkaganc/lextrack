from dal.db import call_proc, call_proc_void

def listele():          return call_proc('sp_DurusmaListele')
def dava_durusmalari(dava_id): return call_proc('sp_DavaDurusmalari', (dava_id,))
def ekle(dava_id,tarih,notlar):
    r = call_proc('sp_DurusmaEkle', (dava_id,tarih,notlar))
    return r[0]['yeni_id'] if r else None
def guncelle(id,tarih,sonuc,notlar,durum):
    call_proc_void('sp_DurusmaGuncelle', (id,tarih,sonuc,notlar,durum))
def sil(id):            call_proc_void('sp_DurusmaSil', (id,))
