from database.db_connection import get_connection

def find_user(username, password):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM users
        WHERE username=%s AND password=%s
    """, (username, password))

    user = cur.fetchone()
    cur.close()
    conn.close()
    return user
