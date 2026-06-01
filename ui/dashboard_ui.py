# ui/dashboard_ui.py — Dashboard (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

import bll.services as svc


class StatCard(QFrame):
    def __init__(self, title, value, icon, color):
        super().__init__()
        self.setObjectName('card')
        self.setMinimumSize(180, 110)
        self.setStyleSheet(
            f'QFrame#card {{ background: {color}; border-radius:10px; border:none; }}'
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet('font-size:26px; color: rgba(255,255,255,0.5);')
        icon_lbl.setAlignment(Qt.AlignLeft)

        lbl_val = QLabel(str(value))
        lbl_val.setFont(QFont('Segoe UI', 26, QFont.Bold))
        lbl_val.setStyleSheet('color:white; font-size:26px; font-weight:bold;')

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet('color:rgba(255,255,255,0.85); font-size:12px;')

        layout.addWidget(icon_lbl)
        layout.addWidget(lbl_val)
        layout.addWidget(lbl_title)


class DashboardWidget(QWidget):
    # Sayfa geçişi için sinyal: hangi sayfaya gidileceğini MainWindow'a bildirir
    navigate = pyqtSignal(int)

    # Sayfa indeksleri (MainWindow'daki stack sırası)
    PAGE_MUSTERILER = 1
    PAGE_AVUKATLAR  = 2
    PAGE_DAVALAR    = 3
    PAGE_DURUSMALAR = 4
    PAGE_GOREVLER   = 5
    PAGE_ODEMELER   = 6

    def __init__(self):
        super().__init__()
        self.setObjectName('content_area')
        self._setup_ui()
        self.load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        # Başlık
        hdr = QVBoxLayout()
        t = QLabel('Dashboard')
        t.setFont(QFont('Segoe UI', 20, QFont.Bold))
        t.setStyleSheet('color: #1e3a5f;')
        s = QLabel('LexTrack — Hukuk Bürosu Dava Takip Sistemi')
        s.setStyleSheet('color: #64748b; font-size:13px;')
        hdr.addWidget(t)
        hdr.addWidget(s)
        layout.addLayout(hdr)

        # İstatistik kartları
        self.card_grid = QGridLayout()
        self.card_grid.setSpacing(14)
        layout.addLayout(self.card_grid)

        # Hızlı erişim başlığı
        quick_title = QLabel('Hızlı Erişim')
        quick_title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        quick_title.setStyleSheet('color: #1e3a5f; margin-top: 8px;')
        layout.addWidget(quick_title)

        # Hızlı erişim butonları — her biri navigate sinyali yayar
        quick_row = QHBoxLayout()
        quick_items = [
            ('📁  Yeni Dava Aç',   '#0369a1', self.PAGE_DAVALAR),
            ('👥  Müşteri Ekle',   '#059669', self.PAGE_MUSTERILER),
            ('📅  Duruşmalar',     '#7c3aed', self.PAGE_DURUSMALAR),
            ('✅  Görevler',       '#d97706', self.PAGE_GOREVLER),
        ]
        for text, color, page_idx in quick_items:
            btn = QPushButton(text)
            btn.setStyleSheet(
                f'background:{color}; color:white; border:none; padding:14px 22px;'
                f'border-radius:8px; font-size:14px; font-weight:bold;'
                f'cursor:pointer;'
            )
            btn.setCursor(Qt.PointingHandCursor)
            # Lambda ile doğru sayfa indeksini yakala
            btn.clicked.connect(lambda _, idx=page_idx: self.navigate.emit(idx))
            quick_row.addWidget(btn)

        layout.addLayout(quick_row)
        layout.addStretch()

    def load_data(self):
        try:
            ist = svc.dashboard_istatistik()
            # Eski kartları temizle
            for i in reversed(range(self.card_grid.count())):
                w = self.card_grid.itemAt(i).widget()
                if w:
                    w.setParent(None)

            cards = [
                ('Kayıtlı Müşteri', int(ist.get('toplam_musteri', 0)), '👥', '#1e3a5f'),
                ('Toplam Dava',      int(ist.get('toplam_dava', 0)),    '📁', '#0369a1'),
                ('Aktif Dava',       int(ist.get('aktif_dava', 0)),     '⚖',  '#b45309'),
                ('Bugün Duruşma',    int(ist.get('bugun_durusma', 0)),  '📅', '#7c3aed'),
                ('Gecikmiş Görev',   int(ist.get('gecmis_gorev', 0)),   '⚠',  '#dc2626'),
                ('Bu Ay Gelir (₺)',  int(ist.get('bu_ay_gelir', 0)),    '💰', '#059669'),
            ]
            for i, (title, val, icon, color) in enumerate(cards):
                self.card_grid.addWidget(StatCard(title, val, icon, color), 0, i)
        except Exception:
            pass
