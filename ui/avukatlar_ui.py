# ui/avukatlar_ui.py — Avukatlar CRUD (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QCheckBox, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.base_widget import BaseTableWidget
import bll.services as svc


class AvukatlarWidget(BaseTableWidget):
    TITLE    = '👔  Avukatlar'
    SUBTITLE = 'Avukat kayıtlarını yönetin'
    COLUMNS  = ['ID', 'Ad', 'Soyad', 'Baro No', 'Uzmanlık', 'Telefon', 'E-Posta', 'Durum']
    DATA_KEYS = ['avukat_id', 'ad', 'soyad', 'baro_no', 'uzmanlik', 'telefon', 'email', 'aktif']

    def load_data(self):
        try:
            records = svc.avukat_listele()
            # Durum sütununu güzelleştir
            for r in records:
                r['aktif'] = 'Aktif' if r.get('aktif') else 'Pasif'
            self.fill_table(records)
        except Exception as e:
            self.show_error(f'Veriler yüklenemedi:\n{e}')

    def on_ekle(self):
        dlg = AvukatForm(self)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.avukat_ekle(dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def on_duzenle(self):
        rec = self.get_selected_record()
        if not rec:
            return
        # Aktif değerini düzelt (string ise)
        rec2 = dict(rec)
        rec2['aktif'] = 1 if rec2.get('aktif') in (1, 'Aktif', True) else 0
        dlg = AvukatForm(self, rec2)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.avukat_guncelle(rec['avukat_id'], dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def _do_sil(self, rec):
        try:
            svc.avukat_sil(rec['avukat_id'])
        except Exception as e:
            self.show_error(str(e))


class AvukatForm(QDialog):
    UZMANLIKLAR = [
        'Ceza Hukuku', 'Is Hukuku', 'Aile Hukuku',
        'Ticaret Hukuku', 'Idare Hukuku', 'Icra Hukuku', 'Genel Hukuk'
    ]

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle('Avukat Ekle' if data is None else 'Avukatı Düzenle')
        self.setMinimumWidth(420)
        self.setModal(True)
        self._build(data)

    def _build(self, d):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel(self.windowTitle())
        title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title.setStyleSheet('color: #1e3a5f; margin-bottom: 6px;')
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.f_ad       = QLineEdit(d['ad']       if d else '')
        self.f_soyad    = QLineEdit(d['soyad']    if d else '')
        self.f_baro     = QLineEdit(d['baro_no']  if d else '')
        self.f_uzmanlik = QComboBox()
        self.f_uzmanlik.addItems(self.UZMANLIKLAR)
        if d:
            i = self.f_uzmanlik.findText(d.get('uzmanlik', ''))
            if i >= 0: self.f_uzmanlik.setCurrentIndex(i)
        self.f_tel      = QLineEdit(d['telefon']  if d else '')
        self.f_email    = QLineEdit(d['email']    if d else '')
        self.f_aktif    = QCheckBox('Aktif')
        self.f_aktif.setChecked(bool(d.get('aktif', 1)) if d else True)

        form.addRow('Ad *',       self.f_ad)
        form.addRow('Soyad *',    self.f_soyad)
        form.addRow('Baro No *',  self.f_baro)
        form.addRow('Uzmanlık',   self.f_uzmanlik)
        form.addRow('Telefon',    self.f_tel)
        form.addRow('E-Posta',    self.f_email)
        form.addRow('Durum',      self.f_aktif)
        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.button(QDialogButtonBox.Save).setText('Kaydet')
        btn_box.button(QDialogButtonBox.Cancel).setText('İptal')
        btn_box.accepted.connect(self._validate)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _validate(self):
        if not self.f_ad.text().strip() or not self.f_soyad.text().strip():
            QMessageBox.warning(self, 'Uyarı', 'Ad ve Soyad zorunludur!')
            return
        if not self.f_baro.text().strip():
            QMessageBox.warning(self, 'Uyarı', 'Baro No zorunludur!')
            return
        self.accept()

    def get_data(self):
        return {
            'ad':        self.f_ad.text().strip(),
            'soyad':     self.f_soyad.text().strip(),
            'baro_no':   self.f_baro.text().strip(),
            'uzmanlik':  self.f_uzmanlik.currentText(),
            'telefon':   self.f_tel.text().strip(),
            'email':     self.f_email.text().strip(),
            'aktif':     '1' if self.f_aktif.isChecked() else '0',
        }
