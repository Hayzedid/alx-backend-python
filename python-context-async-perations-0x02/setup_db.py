import sqlite3

# Create database with proper schema
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Drop existing table and recreate with age column
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INTEGER
)''')

# Insert test data
test_users = [
    ('John Doe', 'john@example.com', 30),
    ('Jane Smith', 'jane@example.com', 45),
    ('Bob Wilson', 'bob@example.com', 50),
    ('Alice Brown', 'alice@example.com', 22),
    ('Charlie Davis', 'charlie@example.com', 35),
    ('Diana Miller', 'diana@example.com', 42)
]

for name, email, age in test_users:
    cursor.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', (name, email, age))

conn.commit()
conn.close()
print('Database created successfully with test data')
