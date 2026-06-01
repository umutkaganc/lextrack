from dal.db import call_proc, call_proc_void

def dava_masraflari(dava_id): return call_proc('sp_DavaMasraflari', (dava_id,))
def ekle(dava_id,aciklama,tutar,tarih,tur):
    r = call_proc('sp_MasrafEkle', (dava_id,aciklama,tutar,tarih,tur))
    return r[0]['yeni_id'] if r else None
def guncelle(id,aciklama,tutar,tarih,tur):
    call_proc_void('sp_MasrafGuncelle', (id,aciklama,tutar,tarih,tur))
def sil(id):            call_proc_void('sp_MasrafSil', (id,))
