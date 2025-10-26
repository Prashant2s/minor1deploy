#!/usr/bin/env python3
"""
SQLite migration helper to add missing columns to the 'certificates' table.
- Adds 'user_id' INTEGER if missing
- Adds 'original_filename' VARCHAR(255) if missing
- Creates index on 'user_id' if missing

Usage:
  python backend/sqlite_add_missing_columns.py --db <path_to_sqlite_db>
If --db is omitted, the script attempts to parse DB_URL from the environment
(e.g., sqlite:///./university.db) and falls back to './university.db'.
"""
import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

def parse_db_path_from_env() -> Path:
    db_url = os.environ.get("DB_URL", "sqlite:///./university.db")
    # Expect forms:
    #  - sqlite:///relative/or/absolute/path.db
    #  - sqlite:////C:/absolute/windows/path.db
    if not db_url.startswith("sqlite"):
        raise ValueError(f"Unsupported DB_URL scheme for this script: {db_url}")

    # Remove sqlite:///
    path_part = db_url.split("sqlite:///")[-1]

    # On Windows, sometimes absolute looks like /C:/path... -> strip leading slash
    if os.name == "nt" and re.match(r"^/[A-Za-z]:/", path_part):
        path_part = path_part[1:]

    return Path(path_part).resolve()

def ensure_columns(db_path: Path) -> None:
    if not db_path.exists():
        print(f"[INFO] Database does not exist at {db_path}. Nothing to migrate.")
        return

    print(f"[INFO] Connecting to SQLite DB: {db_path}")
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        # Ensure table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='certificates';")
        row = cur.fetchone()
        if not row:
            print("[WARN] Table 'certificates' does not exist. Skipping.")
            return

        # Inspect columns
        cur.execute("PRAGMA table_info(certificates);")
        cols = {r[1] for r in cur.fetchall()}  # r[1] is column name
        to_add = []
        if 'user_id' not in cols:
            to_add.append("ALTER TABLE certificates ADD COLUMN user_id INTEGER;")
        if 'original_filename' not in cols:
            to_add.append("ALTER TABLE certificates ADD COLUMN original_filename VARCHAR(255);")

        for stmt in to_add:
            print(f"[INFO] Executing: {stmt.strip()}")
            cur.execute(stmt)

        # Create index for user_id if missing
        print("[INFO] Ensuring index 'idx_certificates_user_id' exists...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_certificates_user_id ON certificates (user_id);")

        conn.commit()
        if to_add:
            print("[SUCCESS] Migration applied. Added columns: " + ", ".join(
                [s.split()[3] for s in to_add]  # crude parse to list column names
            ))
        else:
            print("[INFO] No changes needed. Columns already present.")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=str, default=None, help="Path to SQLite DB file")
    args = parser.parse_args()

    if args.db:
        db_path = Path(args.db).expanduser().resolve()
    else:
        db_path = parse_db_path_from_env()

    ensure_columns(db_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        sys.exit(1)
