from connection import connect_to_fantasyDB
from werkzeug.security import generate_password_hash

def update_password(user_id, password):
    conn = connect_to_fantasyDB()

    cur = conn.cursor()

    try:
        # Hash password
        hashed_password = generate_password_hash(password)

        # Update password
        cur.execute("""
            UPDATE users
            SET password = %s
            WHERE user_id = %s
        """, (hashed_password, user_id))

        conn.commit()

        print("Successfully updated password")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        cur.close()

if __name__ == "__main__":
    update_password(0000, "Password")
