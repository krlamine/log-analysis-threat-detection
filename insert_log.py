import pyodbc
from datetime import datetime
import random


def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=log_threat_detection;'
        'Trusted_Connection=yes;'
    )


def insert_event(cursor, ip, user, status):
    cursor.execute(
        "INSERT INTO log_events VALUES (?, ?, ?, ?, ?)",
        (datetime.now(), ip, user, status, "ssh_login")
    )


def simulate_attacks():
    conn = get_connection()
    cursor = conn.cursor()

    # attacker: brute force + success
    ip = "192.168.1.10"
    for _ in range(7):
        insert_event(cursor, ip, "admin", "failed")
    insert_event(cursor, ip, "admin", "success")

    # attacker: brute force only
    ip = "192.168.1.20"
    for _ in range(8):
        insert_event(cursor, ip, "root", "failed")

    # attacker: mixed behavior
    ip = "192.168.1.30"
    for _ in range(5):
        status = random.choice(["failed", "failed", "success"])
        insert_event(cursor, ip, "user", status)

    # normal user mistakes
    ip = "192.168.1.40"
    for _ in range(2):
        insert_event(cursor, ip, "user", "failed")

    # legitimate login
    ip = "192.168.1.50"
    insert_event(cursor, ip, "user", "success")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    simulate_attacks()
    print("Attack simulation completed.")