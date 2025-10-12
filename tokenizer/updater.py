import sqlite3
import time
from datetime import datetime, timedelta

DB_PATH = r"db.sqlite3"
TABLE_NAME = "core_token"
COLUMN_NUMBER = "number"
COLUMN_LAST_UPDATE = "date"  # new column to store last update date

MAX_NUMBER = 999  # maximum value before wrapping


def update_token():
    """Increment first token's number by 20 with wrap at MAX_NUMBER and store last update date"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Make sure the last_update column exists
    cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
    columns = [col[1] for col in cursor.fetchall()]
    if COLUMN_LAST_UPDATE not in columns:
        cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {COLUMN_LAST_UPDATE} TEXT")
        conn.commit()

    # Get the first token
    cursor.execute(f"SELECT id, {COLUMN_NUMBER} FROM {TABLE_NAME}")
    row = cursor.fetchone()
    if row:
        token_id, number = row
        try:
            current = int(number)
            new_number = (current + 20) % (MAX_NUMBER + 1)
            new_number_str = f"{new_number:03d}"  # zero-padded
            last_update_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                f"UPDATE {TABLE_NAME} SET {COLUMN_NUMBER}=?, {COLUMN_LAST_UPDATE}=? WHERE id=?",
                (new_number_str, last_update_date, token_id)
            )
            conn.commit()
            print(f"[{datetime.now()}] Token {token_id} updated: {number} → {new_number_str}, last_update={last_update_date}")
        except ValueError:
            print(f"[{datetime.now()}] Token number is not numeric: {number}")
    else:
        print(f"[{datetime.now()}] No token found to update.")

    conn.close()


def wait_until_next_friday():
    """Calculate seconds until next Friday 00:00"""
    now = datetime.now()
    days_ahead = 4 - now.weekday()  # Friday=4
    if days_ahead < 0:
        days_ahead += 7
    next_friday = datetime.combine(now.date() + timedelta(days=days_ahead), datetime.min.time())
    seconds_to_wait = (next_friday - now).total_seconds()
    return seconds_to_wait


if __name__ == "__main__":
    while True:
        seconds = wait_until_next_friday()
        print(f"[{datetime.now()}] Sleeping {int(seconds)} seconds until next Friday...")
        time.sleep(seconds)
        if datetime.now().weekday() == 6:
            update_token()
