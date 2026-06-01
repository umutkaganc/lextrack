# ui/gorevler_ui.py — Görevler (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

from ui.base_widget import BaseTableWidget
import bll.services as svc


class GorevlerWidget(BaseTableWidget):
    TITLE     = '✅  Görevler'
    SUBTITLE  = 'Avukatlara atanan görevler'
    COLUMNS   = ['ID', 'Açıklama', 'Dava No', 'Müşteri', 'Avukat', 'Son Tarih', 'Durum']
    DATA_KEYS = ['gorev_id', 'aciklama', 'dava_no', 'musteri_adi', 'avukat_adi', 'son_tarih', 'durum']

    def load_data(self):
        try:
            self.fill_table(svc.gorev_listele())
        except Exception as e:
            self.show_error(f'Veriler yüklenemedi:\n{e}')

    def on_ekle(self):
        davalar   = svc.dava_listele()
        avukatlar = [a for a in svc.avukat_listele() if a.get('aktif') in (1, 'Aktif', True)]
        dlg = GorevForm(self, davalar=davalar, avukatlar=avukatlar)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.gorev_ekle(dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def on_duzenle(self):
        rec = self.get_selected_record()
        if not rec:
            return
        dlg = GorevForm(self, data=rec)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.gorev_guncelle(rec['gorev_id'], dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def _do_sil(self, rec):
        try:
            svc.gorev_sil(rec['gorev_id'])
        except Exception as e:
            self.show_error(str(e))


class GorevForm(QDialog):
    def __init__(self, parent=None, data=None, davalar=None, avukatlar=None):
        super().__init__(parent)
        self.setWindowTitle('Görev Ekle' if data is None else 'Görevi Güncelle')
        self.setMinimumWidth(440)
        self.setModal(True)
        self._davalar   = davalar   or []
        self._avukatlar = avukatlar or []
        self._build(data)

    def _build(self, d):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel(self.windowTitle())
        title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title.setStyleSheet('color: #1e3a5f;')
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.f_dava     = QComboBox()
        for dv in self._davalar:
            self.f_dava.addItem(f"{dv['dava_no']} — {dv.get('musteri_adi','')}", dv['dava_id'])

        self.f_avukat   = QComboBox()
        for av in self._avukatlar:
            self.f_avukat.addItem(f"{av['ad']} {av['soyad']}", av['avukat_id'])

        self.f_aciklama = QTextEdit()
        self.f_aciklama.setFixedHeight(70)
        if d and d.get('aciklama'):
            self.f_aciklama.setPlainText(str(d['aciklama']))

        self.f_tarih = QDateEdit(QDate.currentDate())
        self.f_tarih.setCalendarPopup(True)

        self.f_durum = QComboBox()
        self.f_durum.addItems(['Bekliyor', 'Devam Ediyor', 'Tamamlandi', 'Iptal'])
        if d:
            di = self.f_durum.findText(d.get('durum', ''))
            if di >= 0: self.f_durum.setCurrentIndex(di)

        if not d:
            form.addRow('Dava *',     self.f_dava)
            form.addRow('Avukat *',   self.f_avukat)
        form.addRow('Açıklama *',     self.f_aciklama)
        form.addRow('Son Tarih',      self.f_tarih)
        form.addRow('Durum',          self.f_durum)
        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.button(QDialogButtonBox.Save).setText('Kaydet')
        btn_box.button(QDialogButtonBox.Cancel).setText('İptal')
        btn_box.accepted.connect(self._validate)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _validate(self):
        if not self.f_aciklama.toPlainText().strip():
            QMessageBox.warning(self, 'Uyarı', 'Açıklama zorunludur!')
            return
        self.accept()

    def get_data(self):
        return {
            'dava_id':   self.f_dava.currentData() if self._davalar else None,
            'avukat_id': self.f_avukat.currentData() if self._avukatlar else None,
            'aciklama':  self.f_aciklama.toPlainText().strip(),
            'son_tarih': self.f_tarih.date().toString('yyyy-MM-dd'),
            'durum':     self.f_durum.currentText(),
        }
