# dal/db.py — Veritabanı bağlantı yöneticisi
# KURAL: Tüm DB işlemleri SADECE DAL içinde, SADECE Stored Procedure ile!

import mysql.connector
from config import Config


def get_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST, port=Config.DB_PORT,
        user=Config.DB_USER, password=Config.DB_PASSWORD,
        database=Config.DB_NAME, charset=Config.DB_CHARSET,
        use_unicode=True
    )


def call_proc(proc_name: str, params: tuple = ()):
    """SP çağırır, dict listesi döndürür."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc(proc_name, params)
        rows = []
        for result in cursor.stored_results():
            rows = result.fetchall()
            break
        conn.commit()
        return rows
    except mysql.connector.Error as e:
        conn.rollback(); raise e
    finally:
        cursor.close(); conn.close()


def call_proc_void(proc_name: str, params: tuple = ()):
    """Sonuç döndürmeyen SP'ler için."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(proc_name, params)
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback(); raise e
    finally:
        cursor.close(); conn.close()
