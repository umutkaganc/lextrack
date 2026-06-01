# main.py — LexTrack Hukuk Bürosu Dava Takip Sistemi
# Başlangıç noktası — PyQt5 Masaüstü Uygulaması

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QFont
from ui.style import STYLE
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('LexTrack')
    app.setOrganizationName('BTS304')

    # Global font ve stil
    app.setFont(QFont('Segoe UI', 10))
    app.setStyleSheet(STYLE)

    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        traceback.print_exc()
        QMessageBox.critical(None, 'Başlatma Hatası',
            f'Uygulama başlatılamadı:\n\n{e}\n\n'
            f'config.py dosyasında MySQL bilgilerinizi kontrol edin.')
        sys.exit(1)


if __name__ == '__main__':
    main()
