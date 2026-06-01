from dal.db import call_proc, call_proc_void

def listele():          return call_proc('sp_OdemeListele')
def dava_odemeleri(dava_id): return call_proc('sp_DavaOdemeleri', (dava_id,))
def ekle(musteri_id,dava_id,tutar,tur,aciklama):
    r = call_proc('sp_OdemeEkle', (musteri_id,dava_id,tutar,tur,aciklama))
    return r[0]['yeni_id'] if r else None
def guncelle(id,tutar,tur,aciklama):
    call_proc_void('sp_OdemeGuncelle', (id,tutar,tur,aciklama))
def sil(id):            call_proc_void('sp_OdemeSil', (id,))
