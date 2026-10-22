import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "campus_lost_found.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,           -- 'Lost' or 'Found'
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            date_event TEXT,
            contact_name TEXT,
            contact_info TEXT,
            description TEXT,
            status TEXT DEFAULT 'Open',    -- 'Open' or 'Resolved'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Check if empty, populate initial sample items for demo
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_items = [
            (
                "Lost",
                "Blue Hydro Flask",
                "Water Bottle",
                "Central Library, 2nd Floor",
                datetime.now().strftime("%Y-%m-%d"),
                "Alex Johnson",
                "alex.j@campus.edu",
                "Dark blue 32oz bottle with stickers including NASA and Python logo.",
                "Open"
            ),
            (
                "Found",
                "Student ID Card",
                "ID Card",
                "Student Center Cafeteria",
                datetime.now().strftime("%Y-%m-%d"),
                "Campus Security",
                "security@campus.edu",
                "ID belongs to Priya Sharma, Dept of Computer Science. Kept at Security Desk #2.",
                "Open"
            ),
            (
                "Lost",
                "Sony WH-1000XM4 Headphones",
                "Electronics",
                "Science Block B, Room 204",
                datetime.now().strftime("%Y-%m-%d"),
                "Michael Chen",
                "mchen@campus.edu",
                "Black noise-cancelling headphones in a grey zippered case.",
                "Open"
            ),
            (
                "Found",
                "Calculus 8th Edition Textbook",
                "Books",
                "Math Building bench",
                datetime.now().strftime("%Y-%m-%d"),
                "Library Reception",
                "lib-lostfound@campus.edu",
                "Hardcover Stewart Calculus book with handwritten notes inside cover.",
                "Open"
            ),
        ]
        cursor.executemany("""
            INSERT INTO items (
                type, name, category, location, date_event, 
                contact_name, contact_info, description, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_items)
        conn.commit()
    conn.close()

def add_item(item_type, name, category, location, date_event, contact_name, contact_info, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO items (
            type, name, category, location, date_event,
            contact_name, contact_info, description, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Open')
    """, (item_type, name, category, location, str(date_event), contact_name, contact_info, description))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id

def get_items(search_query="", item_type="All", category="All", status="All"):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM items WHERE 1=1"
    params = []

    if search_query:
        query += " AND (name LIKE ? OR location LIKE ? OR description LIKE ?)"
        term = f"%{search_query.strip()}%"
        params.extend([term, term, term])

    if item_type and item_type != "All":
        query += " AND type = ?"
        params.append(item_type)

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    if status and status != "All":
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_item_status(item_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET status = ? WHERE id = ?", (new_status, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM items")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM items WHERE type = 'Lost' AND status = 'Open'")
    open_lost = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM items WHERE type = 'Found' AND status = 'Open'")
    open_found = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM items WHERE status = 'Resolved'")
    resolved = cursor.fetchone()[0]

    conn.close()
    return {
        "total": total,
        "lost": open_lost,
        "found": open_found,
        "resolved": resolved
    }
