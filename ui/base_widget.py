# ui/base_widget.py — Yeniden Kullanılabilir CRUD Taban Sınıfı

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QHeaderView,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class BaseTableWidget(QWidget):
    """Her entity için ortak tablo + buton düzeni."""

    COLUMNS     = []   # sütun başlıkları
    DATA_KEYS   = []   # veri sözlüğü anahtarları
    TITLE       = ''
    SUBTITLE    = ''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('content_area')
        self._records = []
        self._setup_ui()
        self.load_data()

    # ── UI KURULUM ────────────────────────────────────────────────────────
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Başlık satırı
        hdr = QHBoxLayout()
        title_box = QVBoxLayout()
        lbl_title = QLabel(self.TITLE)
        lbl_title.setObjectName('page_title')
        lbl_title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title_box.addWidget(lbl_title)
        if self.SUBTITLE:
            lbl_sub = QLabel(self.SUBTITLE)
            lbl_sub.setObjectName('page_sub')
            title_box.addWidget(lbl_sub)
        hdr.addLayout(title_box)
        hdr.addStretch()

        # Butonlar
        self.btn_ekle    = QPushButton('➕  Yeni Ekle')
        self.btn_ekle.setObjectName('btn_ekle')
        self.btn_duzenle = QPushButton('✏️  Düzenle')
        self.btn_sil     = QPushButton('🗑  Sil')
        self.btn_sil.setObjectName('btn_sil')
        self.btn_yenile  = QPushButton('↻  Yenile')
        self.btn_yenile.setObjectName('btn_secondary')

        for b in [self.btn_ekle, self.btn_duzenle, self.btn_sil, self.btn_yenile]:
            b.setMinimumWidth(120)
            hdr.addWidget(b)

        self._add_extra_buttons(hdr)
        layout.addLayout(hdr)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.doubleClicked.connect(self.on_duzenle)
        layout.addWidget(self.table)

        # Sayım etiketi
        self.lbl_count = QLabel('0 kayıt')
        self.lbl_count.setStyleSheet('color: #64748b; font-size: 12px;')
        layout.addWidget(self.lbl_count)

        # Sinyal bağlantıları
        self.btn_ekle.clicked.connect(self.on_ekle)
        self.btn_duzenle.clicked.connect(self.on_duzenle)
        self.btn_sil.clicked.connect(self.on_sil)
        self.btn_yenile.clicked.connect(self.load_data)

    def _add_extra_buttons(self, hdr_layout):
        """Alt sınıflarda ek buton eklemek için override edilebilir."""
        pass

    # ── VERİ YÜKLEME ─────────────────────────────────────────────────────
    def load_data(self):
        """Alt sınıflarda override edilmeli."""
        pass

    def fill_table(self, records):
        """Kayıtları tabloya yazar."""
        self._records = records
        self.table.setRowCount(0)
        for row_data in records:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, key in enumerate(self.DATA_KEYS):
                val = row_data.get(key)
                if val is None:
                    val = ''
                item = QTableWidgetItem(str(val))
                item.setData(Qt.UserRole, row_data)  # tüm satır verisini sakla
                self.table.setItem(row, col, item)
        self.table.setRowCount(len(records))
        self.lbl_count.setText(f'{len(records)} kayıt')

    # ── SEÇILI SATIR ─────────────────────────────────────────────────────
    def get_selected_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin.')
            return None
        item = self.table.item(row, 0)
        return item.data(Qt.UserRole) if item else None

    # ── CRUD OLAYLARI ─────────────────────────────────────────────────────
    def on_ekle(self):
        pass

    def on_duzenle(self):
        pass

    def on_sil(self):
        rec = self.get_selected_record()
        if not rec:
            return
        reply = QMessageBox.question(
            self, 'Silme Onayı',
            'Bu kaydı silmek istediğinize emin misiniz?',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self._do_sil(rec)
            self.load_data()

    def _do_sil(self, rec):
        """Alt sınıflarda override edilmeli."""
        pass

    # ── YARDIMCI ─────────────────────────────────────────────────────────
    def show_error(self, msg):
        QMessageBox.critical(self, 'Hata', str(msg))

    def show_success(self, msg):
        QMessageBox.information(self, 'Başarılı', msg)
