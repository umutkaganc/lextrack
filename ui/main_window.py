# ui/main_window.py — Ana Pencere (Sunum Katmanı)

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.dashboard_ui   import DashboardWidget
from ui.musteriler_ui  import MusterilerWidget
from ui.avukatlar_ui   import AvukatlarWidget
from ui.davalar_ui     import DavalarWidget
from ui.durusmalar_ui  import DurusmalarWidget
from ui.gorevler_ui    import GorevlerWidget
from ui.odemeler_ui    import OdemelerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LexTrack — Hukuk Bürosu Dava Takip Sistemi')
        self.setMinimumSize(1280, 800)
        self.resize(1400, 850)
        self._nav_buttons = []
        self._setup_ui()
        # Başlangıçta Dashboard seçili
        self._navigate(0)

    # ── UI KURULUM ───────────────────────────────────────────────────────
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sol sidebar
        sidebar = self._build_sidebar()
        root.addWidget(sidebar)

        # Sağ içerik alanı
        self.stack = QStackedWidget()
        self.stack.setObjectName('content_area')
        root.addWidget(self.stack)

        # Sayfaları oluştur ve stack'e ekle
        self.dashboard    = DashboardWidget()
        self.pg_musteri   = MusterilerWidget()
        self.pg_avukat    = AvukatlarWidget()
        self.pg_dava      = DavalarWidget()
        self.pg_durusma   = DurusmalarWidget()
        self.pg_gorev     = GorevlerWidget()
        self.pg_odeme     = OdemelerWidget()

        for page in [self.dashboard, self.pg_musteri, self.pg_avukat,
                     self.pg_dava, self.pg_durusma, self.pg_gorev, self.pg_odeme]:
            self.stack.addWidget(page)

        # Dashboard'daki hızlı erişim sinyalini bağla
        self.dashboard.navigate.connect(self._navigate)

        self.statusBar().showMessage('LexTrack — Hukuk Bürosu Yönetim Sistemi')

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setFixedWidth(230)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo / başlık
        brand = QLabel('⚖  LexTrack')
        brand.setObjectName('brand')
        brand.setFont(QFont('Segoe UI', 15, QFont.Bold))
        sub = QLabel('Hukuk Bürosu Sistemi')
        sub.setObjectName('brand_sub')
        layout.addWidget(brand)
        layout.addWidget(sub)

        # Ayraç
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet('background-color: #2d4a6e; max-height:1px;')
        layout.addWidget(line)

        # Navigasyon öğeleri: (etiket, sayfa_indeksi veya None=bölüm başlığı)
        nav_items = [
            ('GENEL',             None),
            ('  🏠  Dashboard',   0),
            ('KAYITLAR',          None),
            ('  👥  Müşteriler',  1),
            ('  👔  Avukatlar',   2),
            ('DAVA İŞLEMLERİ',    None),
            ('  📁  Davalar',     3),
            ('  📅  Duruşmalar',  4),
            ('  ✅  Görevler',    5),
            ('FİNANS',            None),
            ('  💰  Ödemeler',    6),
        ]

        for label, idx in nav_items:
            if idx is None:
                sec = QLabel(label)
                sec.setObjectName('nav_section')
                layout.addWidget(sec)
            else:
                btn = QPushButton(label)
                btn.setCheckable(True)
                btn.setAutoExclusive(True)
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(lambda _, i=idx: self._navigate(i))
                self._nav_buttons.append(btn)
                layout.addWidget(btn)

        layout.addStretch()

        ver = QLabel('v1.0 — BTS304 Final Ödevi')
        ver.setStyleSheet('color: #334155; font-size: 11px; padding: 12px;')
        layout.addWidget(ver)
        return sidebar

    def _navigate(self, page_idx: int):
        """Sayfa geçişi yapar ve ilgili sidebar butonunu işaretler."""
        self.stack.setCurrentIndex(page_idx)
        # Sayfa indeksi = buton indeksi (None'lar çıkarıldıktan sonra sıra eşleşiyor)
        if 0 <= page_idx < len(self._nav_buttons):
            self._nav_buttons[page_idx].setChecked(True)

    def run(self):
        self.show()
