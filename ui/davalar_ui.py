# ui/davalar_ui.py — Davalar CRUD + Detay Penceresi (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QTextEdit, QDialogButtonBox, QVBoxLayout, QHBoxLayout,
    QLabel, QMessageBox, QTabWidget, QWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QDoubleSpinBox,
    QSpinBox, QDateTimeEdit, QFrame
)
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QFont, QColor

from ui.base_widget import BaseTableWidget
import bll.services as svc


DAVA_TURLERI = [
    'Ceza Davasi', 'Is Davasi', 'Bosanma Davasi',
    'Ticari Anlasmazlik', 'Miras Davasi', 'Tazminat Davasi',
    'Icra Takibi', 'Idare Davasi', 'Diger'
]
DURUMLAR = ['Aktif', 'Kazanildi', 'Kaybedildi', 'Uzlasma', 'Durduruldu']
DURUM_RENK = {
    'Aktif': '#1e40af', 'Kazanildi': '#065f46',
    'Kaybedildi': '#991b1b', 'Uzlasma': '#92400e', 'Durduruldu': '#475569'
}


class DavalarWidget(BaseTableWidget):
    TITLE     = '📁  Davalar'
    SUBTITLE  = 'Dava kayıtlarını yönetin'
    COLUMNS   = ['ID', 'Dava No', 'Tür', 'Müşteri', 'Avukat', 'Mahkeme', 'Açılış', 'Durum']
    DATA_KEYS = ['dava_id', 'dava_no', 'dava_turu', 'musteri_adi',
                 'avukat_adi', 'mahkeme', 'acilis_tarihi', 'durum']

    def load_data(self):
        try:
            records = svc.dava_listele()
            for r in records:
                if r.get('acilis_tarihi'):
                    r['acilis_tarihi'] = str(r['acilis_tarihi'])
            self.fill_table(records)
            # Renk ver
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 7)
                if item:
                    durum = item.text()
                    clr = QColor(DURUM_RENK.get(durum, '#334155'))
                    item.setForeground(clr)
        except Exception as e:
            self.show_error(f'Veriler yüklenemedi:\n{e}')

    def _add_extra_buttons(self, hdr):
        self.btn_detay = QPushButton('🔍  Detay / Alt Kayıtlar')
        self.btn_detay.setObjectName('btn_detay')
        self.btn_detay.clicked.connect(self.on_detay)
        hdr.addWidget(self.btn_detay)

    def on_ekle(self):
        musteriler = svc.musteri_listele()
        avukatlar  = [a for a in svc.avukat_listele() if a.get('aktif') in (1, 'Aktif', True)]
        dlg = DavaForm(self, musteriler=musteriler, avukatlar=avukatlar)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.dava_ekle(dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def on_duzenle(self):
        rec = self.get_selected_record()
        if not rec:
            return
        musteriler = svc.musteri_listele()
        avukatlar  = svc.avukat_listele()
        dlg = DavaForm(self, data=rec, musteriler=musteriler, avukatlar=avukatlar)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.dava_guncelle(rec['dava_id'], dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def _do_sil(self, rec):
        try:
            svc.dava_sil(rec['dava_id'])
        except Exception as e:
            self.show_error(str(e))

    def on_detay(self):
        rec = self.get_selected_record()
        if not rec:
            return
        dlg = DavaDetayDialog(self, rec)
        dlg.exec_()
        self.load_data()


# ── DAVA FORMU ─────────────────────────────────────────────────────────────
class DavaForm(QDialog):
    def __init__(self, parent=None, data=None, musteriler=None, avukatlar=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Dava' if data is None else 'Davayı Düzenle')
        self.setMinimumWidth(500)
        self.setModal(True)
        self._musteriler = musteriler or []
        self._avukatlar  = avukatlar  or []
        self._build(data)

    def _build(self, d):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel(self.windowTitle())
        title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title.setStyleSheet('color: #1e3a5f;')
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.f_musteri  = QComboBox()
        self.f_avukat   = QComboBox()
        self.f_dava_no  = QLineEdit(d['dava_no']  if d else '')
        self.f_tur      = QComboBox()
        self.f_tur.addItems(DAVA_TURLERI)
        self.f_mahkeme  = QLineEdit(d['mahkeme']  if d else '')
        self.f_tarih    = QDateEdit()
        self.f_tarih.setCalendarPopup(True)
        self.f_tarih.setDate(QDate.currentDate())
        self.f_durum    = QComboBox()
        self.f_durum.addItems(DURUMLAR)
        self.f_aciklama = QTextEdit()
        self.f_aciklama.setFixedHeight(80)

        for m in self._musteriler:
            self.f_musteri.addItem(f"{m['ad']} {m['soyad']}", m['musteri_id'])
        for a in self._avukatlar:
            self.f_avukat.addItem(f"{a['ad']} {a['soyad']} — {a['uzmanlik']}", a['avukat_id'])

        if d:
            mi = self.f_musteri.findData(d.get('musteri_id'))
            if mi >= 0: self.f_musteri.setCurrentIndex(mi)
            ai = self.f_avukat.findData(d.get('avukat_id'))
            if ai >= 0: self.f_avukat.setCurrentIndex(ai)
            ti = self.f_tur.findText(d.get('dava_turu', ''))
            if ti >= 0: self.f_tur.setCurrentIndex(ti)
            di = self.f_durum.findText(d.get('durum', ''))
            if di >= 0: self.f_durum.setCurrentIndex(di)
            if d.get('aciklama'):
                self.f_aciklama.setPlainText(str(d['aciklama']))

        form.addRow('Müşteri *',    self.f_musteri)
        form.addRow('Avukat *',     self.f_avukat)
        form.addRow('Dava No *',    self.f_dava_no)
        form.addRow('Dava Türü',    self.f_tur)
        form.addRow('Mahkeme',      self.f_mahkeme)
        form.addRow('Açılış Tarihi', self.f_tarih)
        form.addRow('Durum',        self.f_durum)
        form.addRow('Açıklama',     self.f_aciklama)
        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.button(QDialogButtonBox.Save).setText('Kaydet')
        btn_box.button(QDialogButtonBox.Cancel).setText('İptal')
        btn_box.accepted.connect(self._validate)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _validate(self):
        if not self.f_dava_no.text().strip():
            QMessageBox.warning(self, 'Uyarı', 'Dava No zorunludur!')
            return
        if self.f_musteri.count() == 0 or self.f_avukat.count() == 0:
            QMessageBox.warning(self, 'Uyarı', 'Müşteri ve avukat listesi boş!')
            return
        self.accept()

    def get_data(self):
        return {
            'musteri_id':    self.f_musteri.currentData(),
            'avukat_id':     self.f_avukat.currentData(),
            'dava_no':       self.f_dava_no.text().strip(),
            'dava_turu':     self.f_tur.currentText(),
            'mahkeme':       self.f_mahkeme.text().strip(),
            'acilis_tarihi': self.f_tarih.date().toString('yyyy-MM-dd'),
            'durum':         self.f_durum.currentText(),
            'aciklama':      self.f_aciklama.toPlainText().strip(),
        }


# ── DAVA DETAY DİYALOĞU ────────────────────────────────────────────────────
class DavaDetayDialog(QDialog):
    def __init__(self, parent, dava_rec):
        super().__init__(parent)
        self.dava = dava_rec
        self.setWindowTitle(f"Dava Detayı — {dava_rec['dava_no']}")
        self.setMinimumSize(900, 600)
        self.setModal(True)
        self._build()
        self._load_all()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        # Özet
        info = QLabel(
            f"<b>{self.dava['dava_no']}</b> — {self.dava.get('dava_turu','')} "
            f"| Müşteri: {self.dava.get('musteri_adi','')} "
            f"| Avukat: {self.dava.get('avukat_adi','')} "
            f"| <span style='color:#0369a1'>{self.dava.get('durum','')}</span>"
        )
        info.setStyleSheet('font-size:13px; padding: 8px; background:#f0f4f8; border-radius:6px;')
        layout.addWidget(info)

        # Sekmeler
        self.tabs = QTabWidget()
        self.tab_durusma = self._make_tab(['ID','Tarih','Durum','Sonuç','Notlar'])
        self.tab_gorev   = self._make_tab(['ID','Açıklama','Avukat','Son Tarih','Durum'])
        self.tab_belge   = self._make_tab(['ID','Belge Adı','Tür','Açıklama','Yüklenme'])
        self.tab_masraf  = self._make_tab(['ID','Açıklama','Tür','Tarih','Tutar (₺)'])
        self.tab_odeme   = self._make_tab(['ID','Tarih','Tür','Açıklama','Tutar (₺)'])
        self.tabs.addTab(self.tab_durusma, '📅 Duruşmalar')
        self.tabs.addTab(self.tab_gorev,   '✅ Görevler')
        self.tabs.addTab(self.tab_belge,   '📄 Belgeler')
        self.tabs.addTab(self.tab_masraf,  '💸 Masraflar')
        self.tabs.addTab(self.tab_odeme,   '💰 Ödemeler')
        layout.addWidget(self.tabs)

        # Ekleme formları
        self._build_add_forms(layout)

        btn_kapat = QPushButton('Kapat')
        btn_kapat.setObjectName('btn_secondary')
        btn_kapat.clicked.connect(self.accept)
        layout.addWidget(btn_kapat, alignment=Qt.AlignRight)

    def _make_tab(self, cols):
        w = QTableWidget()
        w.setColumnCount(len(cols))
        w.setHorizontalHeaderLabels(cols)
        w.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        w.setSelectionBehavior(QTableWidget.SelectRows)
        w.setEditTriggers(QTableWidget.NoEditTriggers)
        w.setAlternatingRowColors(True)
        w.verticalHeader().setVisible(False)
        return w

    def _fill_tab(self, tbl, rows, keys):
        tbl.setRowCount(0)
        for rd in rows:
            r = tbl.rowCount()
            tbl.insertRow(r)
            for c, k in enumerate(keys):
                val = rd.get(k)
                tbl.setItem(r, c, QTableWidgetItem(str(val) if val is not None else ''))

    def _load_all(self):
        did = self.dava['dava_id']
        try:
            dr = svc.dava_durusmalari(did)
            self._fill_tab(self.tab_durusma, dr,
                           ['durusma_id','durusma_tarihi','durum','sonuc','notlar'])
        except: pass
        try:
            gr = svc.dava_gorevleri(did)
            self._fill_tab(self.tab_gorev, gr,
                           ['gorev_id','aciklama','avukat_adi','son_tarih','durum'])
        except: pass
        try:
            br = svc.dava_belgeleri(did)
            self._fill_tab(self.tab_belge, br,
                           ['belge_id','belge_adi','belge_turu','aciklama','yuklenme_tarihi'])
        except: pass
        try:
            mr = svc.dava_masraflari(did)
            self._fill_tab(self.tab_masraf, mr,
                           ['masraf_id','aciklama','tur','tarih','tutar'])
        except: pass
        try:
            or_ = svc.dava_odemeleri(did)
            self._fill_tab(self.tab_odeme, or_,
                           ['odeme_id','tarih','tur','aciklama','tutar'])
        except: pass

    def _build_add_forms(self, layout):
        """Hızlı ekleme formu."""
        frame = QFrame()
        frame.setStyleSheet('QFrame{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;}')
        fl = QHBoxLayout(frame)
        fl.setContentsMargins(12, 10, 12, 10)
        fl.setSpacing(10)

        # Duruşma ekle
        fl.addWidget(QLabel('<b>Duruşma Ekle:</b>'))
        self.dr_tarih = QDateTimeEdit(QDateTime.currentDateTime())
        self.dr_tarih.setCalendarPopup(True)
        self.dr_tarih.setDisplayFormat('dd.MM.yyyy HH:mm')
        self.dr_notlar = QLineEdit()
        self.dr_notlar.setPlaceholderText('Notlar...')
        btn_dr = QPushButton('+ Duruşma')
        btn_dr.setObjectName('btn_ekle')
        btn_dr.clicked.connect(self._ekle_durusma)
        fl.addWidget(self.dr_tarih)
        fl.addWidget(self.dr_notlar)
        fl.addWidget(btn_dr)

        fl.addWidget(QLabel(' | '))

        # Ödeme ekle
        fl.addWidget(QLabel('<b>Ödeme Ekle (₺):</b>'))
        self.od_tutar = QDoubleSpinBox()
        self.od_tutar.setMaximum(9999999); self.od_tutar.setDecimals(2)
        self.od_tur = QComboBox()
        self.od_tur.addItems(['Nakit','Kredi Karti','Banka Transferi','Cek'])
        btn_od = QPushButton('+ Ödeme')
        btn_od.setObjectName('btn_ekle')
        btn_od.clicked.connect(self._ekle_odeme)
        fl.addWidget(self.od_tutar)
        fl.addWidget(self.od_tur)
        fl.addWidget(btn_od)

        layout.addWidget(frame)

    def _ekle_durusma(self):
        try:
            svc.durusma_ekle({
                'dava_id': self.dava['dava_id'],
                'durusma_tarihi': self.dr_tarih.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
                'notlar': self.dr_notlar.text()
            })
            self._load_all()
            self.dr_notlar.clear()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', str(e))

    def _ekle_odeme(self):
        try:
            svc.odeme_ekle({
                'musteri_id': self.dava['musteri_id'],
                'dava_id':    self.dava['dava_id'],
                'tutar':      str(self.od_tutar.value()),
                'tur':        self.od_tur.currentText(),
                'aciklama':   ''
            })
            self._load_all()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', str(e))
