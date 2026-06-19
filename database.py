import sqlite3

conn = sqlite3.connect("rag_logs.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS query_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer_found INTEGER,
    latency REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def log_query(question, answer_found, latency):
    cursor.execute(
        """
        INSERT INTO query_logs
        (question, answer_found, latency)
        VALUES (?, ?, ?)
        """,
        (question, answer_found, latency)
    )
    conn.commit()





def get_analytics():
    cursor.execute("""
    SELECT question,
    COUNT(*) as count
    FROM query_logs
    GROUP BY question
    ORDER BY count DESC
    LIMIT 5
    """)

    most_frequent = cursor.fetchall()


    cursor.execute("""
    SELECT question
    FROM query_logs
    WHERE answer_found = 0
    """)

    no_answer = cursor.fetchall()


    cursor.execute("""
    SELECT AVG(latency)
    FROM query_logs
    """)

    avg_latency = cursor.fetchone()[0]


    return {
    "most_frequent_questions": most_frequent,
    "no_answer_queries": no_answer,
    "average_latency": avg_latency
}