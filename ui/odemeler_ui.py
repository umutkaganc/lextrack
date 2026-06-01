# ui/odemeler_ui.py — Ödemeler (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox,
    QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.base_widget import BaseTableWidget
import bll.services as svc


class OdemelerWidget(BaseTableWidget):
    TITLE     = '💰  Ödemeler'
    SUBTITLE  = 'Müşteri ödemeleri'
    COLUMNS   = ['ID', 'Tarih', 'Müşteri', 'Dava No', 'Tür', 'Tutar (₺)', 'Açıklama']
    DATA_KEYS = ['odeme_id', 'tarih', 'musteri_adi', 'dava_no', 'tur', 'tutar', 'aciklama']

    def load_data(self):
        try:
            self.fill_table(svc.odeme_listele())
        except Exception as e:
            self.show_error(f'Veriler yüklenemedi:\n{e}')

    def on_ekle(self):
        musteriler = svc.musteri_listele()
        davalar    = svc.dava_listele()
        dlg = OdemeForm(self, musteriler=musteriler, davalar=davalar)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.odeme_ekle(dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def on_duzenle(self):
        QMessageBox.information(self, 'Bilgi',
            'Ödemeleri düzenlemek için lütfen silin ve yeniden ekleyin.')

    def _do_sil(self, rec):
        try:
            svc.odeme_sil(rec['odeme_id'])
        except Exception as e:
            self.show_error(str(e))


class OdemeForm(QDialog):
    def __init__(self, parent=None, musteriler=None, davalar=None):
        super().__init__(parent)
        self.setWindowTitle('Ödeme Ekle')
        self.setMinimumWidth(440)
        self.setModal(True)
        self._musteriler = musteriler or []
        self._davalar    = davalar    or []
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel('Ödeme Ekle')
        title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title.setStyleSheet('color: #1e3a5f;')
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.f_musteri = QComboBox()
        for m in self._musteriler:
            self.f_musteri.addItem(f"{m['ad']} {m['soyad']}", m['musteri_id'])

        self.f_dava = QComboBox()
        for d in self._davalar:
            self.f_dava.addItem(f"{d['dava_no']} — {d.get('musteri_adi','')}", d['dava_id'])

        self.f_tutar = QDoubleSpinBox()
        self.f_tutar.setMaximum(9999999)
        self.f_tutar.setDecimals(2)
        self.f_tutar.setMinimum(0.01)

        self.f_tur = QComboBox()
        self.f_tur.addItems(['Nakit', 'Kredi Karti', 'Banka Transferi', 'Cek'])

        self.f_aciklama = QLineEdit()

        form.addRow('Müşteri *',  self.f_musteri)
        form.addRow('Dava *',     self.f_dava)
        form.addRow('Tutar (₺) *', self.f_tutar)
        form.addRow('Ödeme Türü', self.f_tur)
        form.addRow('Açıklama',   self.f_aciklama)
        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.button(QDialogButtonBox.Save).setText('Kaydet')
        btn_box.button(QDialogButtonBox.Cancel).setText('İptal')
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_data(self):
        return {
            'musteri_id': self.f_musteri.currentData(),
            'dava_id':    self.f_dava.currentData(),
            'tutar':      str(self.f_tutar.value()),
            'tur':        self.f_tur.currentText(),
            'aciklama':   self.f_aciklama.text().strip(),
        }
