import sqlite3


def create_database():
    conn = sqlite3.connect("data/reviews.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            review TEXT,
            sentiment TEXT,
            polarity REAL
        )
    """)

    conn.commit()
    conn.close()


def save_review(product, review, sentiment, polarity):
    conn = sqlite3.connect("data/reviews.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews
        (product, review, sentiment, polarity)
        VALUES (?, ?, ?, ?)
    """, (product, review, sentiment, polarity))

    conn.commit()
    conn.close()