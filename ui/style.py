# ui/style.py — Global QSS Stili

STYLE = """
* {
    font-family: 'Segoe UI', 'Arial';
    font-size: 13px;
}
QMainWindow {
    background-color: #f0f4f8;
}

/* ── SIDEBAR ── */
QFrame#sidebar {
    background-color: #1e3a5f;
    border-right: 2px solid #162d4a;
}
QLabel#brand {
    color: #c9a84c;
    font-size: 16px;
    font-weight: bold;
    padding: 20px 16px 4px 16px;
}
QLabel#brand_sub {
    color: #64748b;
    font-size: 11px;
    padding: 0px 16px 16px 16px;
}
QFrame#sidebar QPushButton {
    background: transparent;
    color: #cbd5e1;
    border: none;
    text-align: left;
    padding: 11px 16px;
    font-size: 13px;
    border-radius: 6px;
    margin: 2px 8px;
}
QFrame#sidebar QPushButton:hover {
    background: rgba(201, 168, 76, 0.18);
    color: #f1c40f;
}
QFrame#sidebar QPushButton:checked {
    background: rgba(201, 168, 76, 0.25);
    color: #f1c40f;
    font-weight: bold;
}
QLabel#nav_section {
    color: #475569;
    font-size: 10px;
    font-weight: bold;
    padding: 12px 18px 4px 18px;
    letter-spacing: 1px;
}

/* ── İÇERİK ALANI ── */
QWidget#content_area {
    background-color: #f0f4f8;
}
QLabel#page_title {
    font-size: 20px;
    font-weight: bold;
    color: #1e3a5f;
}
QLabel#page_sub {
    font-size: 12px;
    color: #64748b;
}

/* ── KARTLAR ── */
QFrame#card {
    background: white;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
}
QLabel#stat_value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}
QLabel#stat_label {
    font-size: 12px;
    color: rgba(255,255,255,0.8);
}

/* ── TABLO ── */
QTableWidget {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f0f4f8;
    selection-background-color: #dbeafe;
    selection-color: #1e40af;
    alternate-background-color: #f8fafc;
}
QTableWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #f0f4f8;
    color: #334155;
}
QTableWidget::item:selected {
    background: #dbeafe;
    color: #1e40af;
}
QHeaderView::section {
    background: #f0f4f8;
    color: #1e3a5f;
    font-weight: bold;
    padding: 10px 12px;
    border: none;
    border-right: 1px solid #e2e8f0;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── BUTONLAR ── */
QPushButton {
    background: #1e3a5f;
    color: white;
    border: none;
    padding: 9px 20px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover { background: #162d4a; }
QPushButton:pressed { background: #0f1d30; }
QPushButton#btn_ekle {
    background: #059669;
}
QPushButton#btn_ekle:hover { background: #047857; }
QPushButton#btn_sil {
    background: #dc2626;
}
QPushButton#btn_sil:hover { background: #b91c1c; }
QPushButton#btn_detay {
    background: #7c3aed;
}
QPushButton#btn_detay:hover { background: #6d28d9; }
QPushButton#btn_secondary {
    background: #64748b;
}
QPushButton#btn_secondary:hover { background: #475569; }

/* ── FORMLAR ── */
QDialog {
    background: white;
}
QLabel#form_label {
    font-weight: bold;
    color: #374151;
}
QLineEdit, QComboBox, QDateEdit, QDateTimeEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    border: 1.5px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 10px;
    background: white;
    color: #1e293b;
    font-size: 13px;
    min-height: 16px;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
    border-color: #1e3a5f;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    border: 1px solid #cbd5e1;
    selection-background-color: #dbeafe;
}

/* ── STATUS BAR ── */
QStatusBar {
    background: #1e3a5f;
    color: #94a3b8;
    font-size: 12px;
}
"""
