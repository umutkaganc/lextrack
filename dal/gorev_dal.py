from dal.db import call_proc, call_proc_void

def listele():          return call_proc('sp_GorevListele')
def dava_gorevleri(dava_id): return call_proc('sp_DavaGorevleri', (dava_id,))
def ekle(dava_id,avukat_id,aciklama,son_tarih):
    r = call_proc('sp_GorevEkle', (dava_id,avukat_id,aciklama,son_tarih))
    return r[0]['yeni_id'] if r else None
def guncelle(id,aciklama,son_tarih,durum):
    call_proc_void('sp_GorevGuncelle', (id,aciklama,son_tarih,durum))
def sil(id):            call_proc_void('sp_GorevSil', (id,))
