# ui/durusmalar_ui.py — Duruşmalar (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox,
    QTextEdit, QDateTimeEdit
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont

from ui.base_widget import BaseTableWidget
import bll.services as svc


class DurusmalarWidget(BaseTableWidget):
    TITLE     = '📅  Duruşmalar'
    SUBTITLE  = 'Tüm duruşma kayıtları'
    COLUMNS   = ['ID', 'Tarih', 'Dava No', 'Müşteri', 'Durum', 'Sonuç', 'Notlar']
    DATA_KEYS = ['durusma_id', 'durusma_tarihi', 'dava_no', 'musteri_adi', 'durum', 'sonuc', 'notlar']

    def load_data(self):
        try:
            self.fill_table(svc.durusma_listele())
        except Exception as e:
            self.show_error(f'Veriler yüklenemedi:\n{e}')

    def on_ekle(self):
        davalar = [d for d in svc.dava_listele() if d.get('durum') == 'Aktif']
        dlg = DurusmaForm(self, davalar=davalar)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.durusma_ekle(dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def on_duzenle(self):
        rec = self.get_selected_record()
        if not rec:
            return
        dlg = DurusmaForm(self, data=rec)
        if dlg.exec_() == QDialog.Accepted:
            try:
                svc.durusma_guncelle(rec['durusma_id'], dlg.get_data())
                self.load_data()
            except Exception as e:
                self.show_error(str(e))

    def _do_sil(self, rec):
        try:
            svc.durusma_sil(rec['durusma_id'])
        except Exception as e:
            self.show_error(str(e))


class DurusmaForm(QDialog):
    def __init__(self, parent=None, data=None, davalar=None):
        super().__init__(parent)
        self.setWindowTitle('Duruşma Ekle' if data is None else 'Duruşmayı Düzenle')
        self.setMinimumWidth(440)
        self.setModal(True)
        self._davalar = davalar or []
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

        self.f_dava   = QComboBox()
        for dv in self._davalar:
            self.f_dava.addItem(f"{dv['dava_no']} — {dv.get('musteri_adi','')}", dv['dava_id'])

        self.f_tarih  = QDateTimeEdit(QDateTime.currentDateTime())
        self.f_tarih.setCalendarPopup(True)
        self.f_tarih.setDisplayFormat('dd.MM.yyyy HH:mm')

        self.f_durum  = QComboBox()
        self.f_durum.addItems(['Planlandi', 'Tamamlandi', 'Ertelendi'])

        self.f_sonuc  = QLineEdit(d.get('sonuc', '') if d else '')
        self.f_notlar = QTextEdit()
        self.f_notlar.setFixedHeight(70)
        if d and d.get('notlar'):
            self.f_notlar.setPlainText(str(d['notlar']))

        if d:
            di = self.f_durum.findText(d.get('durum', ''))
            if di >= 0: self.f_durum.setCurrentIndex(di)

        if not d:
            form.addRow('Dava *',       self.f_dava)
        form.addRow('Tarih/Saat *',     self.f_tarih)
        form.addRow('Durum',            self.f_durum)
        form.addRow('Sonuç',            self.f_sonuc)
        form.addRow('Notlar',           self.f_notlar)
        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.button(QDialogButtonBox.Save).setText('Kaydet')
        btn_box.button(QDialogButtonBox.Cancel).setText('İptal')
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_data(self):
        return {
            'dava_id':         self.f_dava.currentData() if self._davalar else None,
            'durusma_tarihi':  self.f_tarih.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            'durum':           self.f_durum.currentText(),
            'sonuc':           self.f_sonuc.text().strip(),
            'notlar':          self.f_notlar.toPlainText().strip(),
        }
