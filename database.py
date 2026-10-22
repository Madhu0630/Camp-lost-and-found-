import sqlite3
from datetime import datetime
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "campus_lost_found.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a salt."""
    salt = "CampusConnect_Salt_2026"
    return hashlib.sha256((password.strip() + salt).encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',   -- 'admin' or 'student'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Items Table
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
            username TEXT DEFAULT 'Anonymous',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Ensure username column exists if upgrading from an older DB version
    cursor.execute("PRAGMA table_info(items)")
    columns = [col[1] for col in cursor.fetchall()]
    if "username" not in columns:
        cursor.execute("ALTER TABLE items ADD COLUMN username TEXT DEFAULT 'Anonymous'")
        conn.commit()

    # 3. Seed Default Users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        default_users = [
            ("admin", "admin@campus.edu", hash_password("admin123"), "admin"),
            ("student", "student@campus.edu", hash_password("student123"), "student"),
        ]
        cursor.executemany("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, default_users)
        conn.commit()

    # 4. Seed Default Sample Items if empty
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
                "Open",
                "student"
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
                "Open",
                "admin"
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
                "Open",
                "student"
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
                "Open",
                "admin"
            ),
        ]
        cursor.executemany("""
            INSERT INTO items (
                type, name, category, location, date_event, 
                contact_name, contact_info, description, status, username
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_items)
        conn.commit()
    conn.close()

# ----------------- USER AUTHENTICATION -----------------

def register_user(username, email, password, role="student"):
    username = username.strip().lower()
    email = email.strip().lower()

    if not username or not email or not password:
        return False, "All fields are required."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (username, email, hash_password(password), role))
        conn.commit()
        return True, "Account registered successfully! You can now log in."
    except sqlite3.IntegrityError:
        return False, "Username or email is already registered."
    finally:
        conn.close()

def authenticate_user(username_or_email, password):
    term = username_or_email.strip().lower()
    hashed = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, email, role, created_at
        FROM users
        WHERE (username = ? OR email = ?) AND password_hash = ?
    """, (term, term, hashed))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ----------------- ITEM OPERATIONS -----------------

def add_item(item_type, name, category, location, date_event, contact_name, contact_info, description, username="Anonymous"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO items (
            type, name, category, location, date_event,
            contact_name, contact_info, description, status, username
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Open', ?)
    """, (item_type, name, category, location, str(date_event), contact_name, contact_info, description, username))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id

def get_items(search_query="", item_type="All", category="All", status="All", username=None):
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

    if username:
        query += " AND username = ?"
        params.append(username)

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

def get_stats(username=None):
    conn = get_connection()
    cursor = conn.cursor()

    user_clause = " WHERE username = ?" if username else ""
    params = (username,) if username else ()

    cursor.execute(f"SELECT COUNT(*) FROM items{user_clause}", params)
    total = cursor.fetchone()[0]

    if username:
        cursor.execute("SELECT COUNT(*) FROM items WHERE type = 'Lost' AND status = 'Open' AND username = ?", (username,))
        open_lost = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM items WHERE type = 'Found' AND status = 'Open' AND username = ?", (username,))
        open_found = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM items WHERE status = 'Resolved' AND username = ?", (username,))
        resolved = cursor.fetchone()[0]
    else:
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
