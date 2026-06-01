from dal.db import call_proc, call_proc_void

def listele():          return call_proc('sp_DavaListele')
def getir(id):
    r = call_proc('sp_DavaGetir', (id,)); return r[0] if r else None
def ekle(musteri_id,avukat_id,dava_no,dava_turu,mahkeme,acilis_tarihi,aciklama):
    r = call_proc('sp_DavaEkle', (musteri_id,avukat_id,dava_no,dava_turu,mahkeme,acilis_tarihi,aciklama))
    return r[0]['yeni_id'] if r else None
def guncelle(id,musteri_id,avukat_id,dava_no,dava_turu,mahkeme,durum,aciklama):
    call_proc_void('sp_DavaGuncelle', (id,musteri_id,avukat_id,dava_no,dava_turu,mahkeme,durum,aciklama))
def sil(id):            call_proc_void('sp_DavaSil', (id,))
