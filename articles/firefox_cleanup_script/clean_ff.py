#!/usr/bin/env python

import os, sys, subprocess
import sqlite3
from datetime import date, timedelta
import time

# Replace with your user profile, see about:profiles in the browser
PROFILE='/j/.mozilla/firefox/cfzbb6kw.default-release/'

if __name__ == '__main__':
  db = f"{PROFILE}/places.sqlite"
  conn = sqlite3.connect(db);

  today = date.today()
  last_week = today - timedelta(days=7)
  # firefox stores times in epoch nanoseconds (epoch seconds * 1 million)
  oldest_nanoseconds = int( time.mktime(last_week.timetuple()) ) * 1000000
  print(f"oldest_nanoseconds={oldest_nanoseconds}");
  
  # Remove all from moz_bookmarks_deleted
  r = conn.execute("""
delete from moz_bookmarks_deleted where 1=1;
""")
  print(f"moz_bookmarks_deleted r.rowcount={r.rowcount}")

  # Trim moz_historyvisits
  #CREATE TABLE moz_historyvisits (  id INTEGER PRIMARY KEY, from_visit INTEGER, place_id INTEGER, visit_date INTEGER, visit_type INTEGER, session INTEGER);
  r = conn.execute(f"""
delete from moz_historyvisits where visit_date < {oldest_nanoseconds};
""")
  print(f"moz_historyvisits r.rowcount={r.rowcount}")

  # Trim moz_inputhistory
  # CREATE TABLE moz_inputhistory (  place_id INTEGER NOT NULL, input LONGVARCHAR NOT NULL, use_count INTEGER, PRIMARY KEY (place_id, input));
  r = conn.execute("""
delete from moz_inputhistory where use_count < 4;
""")
  print(f"moz_inputhistory r.rowcount={r.rowcount}")
  
  conn.commit()
  conn.close()

  db = f"{PROFILE}/cookies.sqlite"
  conn = sqlite3.connect(db);

  # Remove cookies > 1 month old
  # CREATE TABLE moz_cookies (id INTEGER PRIMARY KEY, originAttributes TEXT NOT NULL DEFAULT '', name TEXT, value TEXT, host TEXT, path TEXT, expiry INTEGER, lastAccessed INTEGER, creationTime INTEGER, isSecure INTEGER, isHttpOnly INTEGER, inBrowserElement INTEGER DEFAULT 0, sameSite INTEGER DEFAULT 0, rawSameSite INTEGER DEFAULT 0, schemeMap INTEGER DEFAULT 0, CONSTRAINT moz_uniqueid UNIQUE (name, host, path, originAttributes));
  r = conn.execute(f"""
delete from moz_cookies where creationTime < {oldest_nanoseconds};
""")
  print(f"moz_cookies r.rowcount={r.rowcount}")

  conn.commit()
  conn.close()

