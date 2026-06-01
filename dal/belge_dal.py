from dal.db import call_proc, call_proc_void

def dava_belgeleri(dava_id): return call_proc('sp_DavaBelgeleri', (dava_id,))
def ekle(dava_id,belge_adi,belge_turu,aciklama):
    r = call_proc('sp_BelgeEkle', (dava_id,belge_adi,belge_turu,aciklama))
    return r[0]['yeni_id'] if r else None
def guncelle(id,belge_adi,belge_turu,aciklama):
    call_proc_void('sp_BelgeGuncelle', (id,belge_adi,belge_turu,aciklama))
def sil(id):            call_proc_void('sp_BelgeSil', (id,))
