from db import get_connection
from datetime import datetime


def calculate_scores(cursor):
    scores = {}

    # count failed attempts per IP
    cursor.execute("""
        SELECT ip, COUNT(*)
        FROM log_events
        WHERE LOWER(status) = 'failed'
        GROUP BY ip
    """)

    for ip, fails in cursor.fetchall():
        if fails <= 2:
            scores[ip] = 1
        elif fails <= 5:
            scores[ip] = 2
        else:
            scores[ip] = 3

    # detect success after multiple failures within short time window
    cursor.execute("""
        SELECT DISTINCT s.ip
        FROM log_events s
        WHERE LOWER(s.status) = 'success'
        AND EXISTS (
            SELECT 1
            FROM log_events f
            WHERE f.ip = s.ip
            AND LOWER(f.status) = 'failed'
            AND f.timestamp BETWEEN DATEADD(MINUTE, -5, s.timestamp) AND s.timestamp
            GROUP BY f.ip
            HAVING COUNT(*) >= 3
        )
    """)

    for (ip,) in cursor.fetchall():
        scores[ip] = scores.get(ip, 0) + 5

    return scores


def analyze_behavior(cursor, ip):
    cursor.execute("""
        SELECT COUNT(*) FROM log_events
        WHERE ip = ? AND LOWER(status) = 'failed'
    """, (ip,))
    fail_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM log_events
        WHERE ip = ? AND LOWER(status) = 'success'
    """, (ip,))
    success_count = cursor.fetchone()[0]

    return fail_count, success_count


def classify_event(score, fail_count, success_count):
    if score >= 7:
        return "CRITICAL 🔥", "Brute force attack succeeded (multiple failures followed by login)"
    elif fail_count >= 5:
        return "HIGH ⚠️", "Repeated failed login attempts (possible brute force)"
    elif fail_count > 0 and success_count > 0:
        return "MEDIUM 🟡", "Mixed login activity (failures + success)"
    elif fail_count > 0:
        return "LOW 🟡", "Few failed login attempts (likely user error)"
    else:
        return "LOW 🟢", "Normal login behavior"


def generate_scored_alerts():
    conn = get_connection()
    cursor = conn.cursor()

    scores = calculate_scores(cursor)

    print("\n=== SOC ALERT REPORT ===\n")

    if not scores:
        print("No suspicious activity detected.")
        return

    report_lines = []

    for ip, score in scores.items():
        fail_count, success_count = analyze_behavior(cursor, ip)
        level, reason = classify_event(score, fail_count, success_count)

        line = f"{level} | IP: {ip} | Score: {score} | Reason: {reason}"
        print(line)
        report_lines.append(line)

    conn.close()

    # save alerts
    with open("alerts_report.txt", "w", encoding="utf-8") as f:
        f.write("=== SOC ALERT REPORT ===\n")
        f.write(f"Generated at: {datetime.now()}\n\n")
        for line in report_lines:
            f.write(line + "\n")


if __name__ == "__main__":
    print("Running scoring engine...\n")
    generate_scored_alerts()