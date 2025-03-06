import sqlite3
import random

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class TEXT NOT NULL,
    subject TEXT NOT NULL,
    marks INTEGER
)
''')

# Sample data
names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ian", "Jack", "Kevin", "Laura", "Mia", "Nina", "Oscar", "Paul", "Quinn", "Rachel", "Steve", "Tina"]
classes = ["DataScience", "Art"]
subjects = ["Math", "Physics", "History", "Literature", "Computer Science"]

# Insert 100 random student records
for i in range(100):
    name = random.choice(names)
    student_class = random.choice(classes)
    subject = random.choice(subjects)
    marks = random.randint(50, 100)
    cursor.execute("INSERT INTO students (name, class, subject, marks) VALUES (?, ?, ?, ?)", 
                   (name, student_class, subject, marks))

# Commit changes
conn.commit()

# Retrieve and display data
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
