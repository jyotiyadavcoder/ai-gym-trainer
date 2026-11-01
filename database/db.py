import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_or_create_user(name, weight=60):
    """Naam se user dhundta hai, na mile to naya bana deta hai."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM users WHERE name = %s", (name,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute(
            "INSERT INTO users (name, weight_kg) VALUES (%s, %s)", (name, weight)
        )
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()


def save_workout(user_id, exercise, reps, duration_sec, calories):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO workouts (user_id, exercise, reps, duration_sec, calories) "
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, exercise, reps, duration_sec, calories),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def get_history(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT exercise, reps, duration_sec, calories, workout_date "
            "FROM workouts WHERE user_id = %s ORDER BY workout_date DESC",
            (user_id,),
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def get_summary(user_id):
    """Total workouts, reps aur calories."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT COUNT(*) AS total_workouts, "
            "COALESCE(SUM(reps), 0) AS total_reps, "
            "COALESCE(SUM(calories), 0) AS total_calories "
            "FROM workouts WHERE user_id = %s",
            (user_id,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()