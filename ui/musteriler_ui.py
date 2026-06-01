# ui/musteriler_ui.py — Müşteriler CRUD (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.base_widget import BaseTableWidget
import bll.services as svc


class MusterilerWidget(BaseTableWidget):
    TITLE     = '👥  Müşteriler'
    SUBTITLE  = 'Müşteri kayıtlarını yönetin'
    COLUMNS   = ['ID', 'Ad', 'Soyad', 'TC Kimlik', 'Telefon', 'E-Posta', 'Adres', 'Kayıt Tarihi']
    DATA_KEYS = ['musteri_id', 'ad', 'soyad', 'tc_no', 'telefon', 'email', 'adres', 'kayit_tarihi']

    def load_data(self):
        try:
            self.fill_table(svc.musteri_listele())
        except Exception as e:
            self.show_error(f'Veriler yüklenemedi:\n{e}')

    def on_ekle(self):
        dlg = MusteriForm(self)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.musteri_ekle(dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def on_duzenle(self):
        rec = self.get_selected_record()
        if not rec:
            return
        dlg = MusteriForm(self, rec)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.musteri_guncelle(rec['musteri_id'], dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def _do_sil(self, rec):
        try:
            svc.musteri_sil(rec['musteri_id'])
        except Exception as e:
            self.show_error(str(e))


class MusteriForm(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle('Müşteri Ekle' if data is None else 'Müşteriyi Düzenle')
        self.setMinimumWidth(440)
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

        self.f_ad     = QLineEdit(d['ad']     if d else '')
        self.f_soyad  = QLineEdit(d['soyad']  if d else '')
        self.f_tc     = QLineEdit(d['tc_no']  if d else '')
        self.f_tc.setMaxLength(11)
        self.f_tel    = QLineEdit(d['telefon'] if d else '')
        self.f_email  = QLineEdit(d['email']  if d else '')
        self.f_adres  = QTextEdit(d['adres']  if d else '')
        self.f_adres.setFixedHeight(70)

        form.addRow('Ad *',          self.f_ad)
        form.addRow('Soyad *',       self.f_soyad)
        form.addRow('TC Kimlik No *', self.f_tc)
        form.addRow('Telefon',       self.f_tel)
        form.addRow('E-Posta',       self.f_email)
        form.addRow('Adres',         self.f_adres)
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
        tc = self.f_tc.text().strip()
        if not tc or len(tc) != 11 or not tc.isdigit():
            QMessageBox.warning(self, 'Uyarı', 'TC Kimlik No 11 haneli rakam olmalıdır!')
            return
        self.accept()

    def get_data(self):
        return {
            'ad':      self.f_ad.text().strip(),
            'soyad':   self.f_soyad.text().strip(),
            'tc_no':   self.f_tc.text().strip(),
            'telefon': self.f_tel.text().strip(),
            'email':   self.f_email.text().strip(),
            'adres':   self.f_adres.toPlainText().strip(),
        }
