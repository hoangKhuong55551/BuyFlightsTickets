"""
backup_db.py - Backup SQLite database
Chay: python backup_db.py
Nen dat vao Task Scheduler chay moi ngay 1 lan.
"""
import shutil, os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_SRC   = BASE_DIR / "db.sqlite3"
BACKUP_DIR = BASE_DIR / "db_backups"

BACKUP_DIR.mkdir(exist_ok=True)

# Giu toi da 30 ban backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
dest = BACKUP_DIR / f"db_{timestamp}.sqlite3"
shutil.copy2(DB_SRC, dest)
print(f"[OK] Backed up to: {dest}")

# Xoa backup cu (giu 30 ban)
backups = sorted(BACKUP_DIR.glob("db_*.sqlite3"))
MAX_BACKUPS = 30
while len(backups) > MAX_BACKUPS:
    old = backups.pop(0)
    old.unlink()
    print(f"[DEL] Removed old backup: {old.name}")