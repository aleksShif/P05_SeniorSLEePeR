import sqlite3

def get_connection(db):
    conn = sqlite3.connect(db)
    return conn


def query_db(query, args=(), all=False):
    conn = get_connection("P5.db")

    with conn:
        cur = conn.cursor()
        r = cur.execute(query, args)
        r = cur.fetchall()
    conn.close()

    return (r[0] if r else None) if not all else r

DB_FILE = "P5.db"
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

