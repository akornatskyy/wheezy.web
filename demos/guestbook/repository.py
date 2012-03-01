from models import Greeting

class Repository(object):

    def __init__(self, db):
        self.db = db

    def list_greetings(self):
        cursor = self.db.execute("""
                SELECT id, created_on, author, message
                FROM greeting
                ORDER BY id DESC
                LIMIT 10
        """)
        return [Greeting(
                id=row[0],
                created_on=row[1],
                author=row[2],
                message=row[3]) for row in cursor.fetchall()]

    def add_greeting(self, greeting):
        self.db.execute("""
                INSERT INTO greeting (created_on, author, message)
                VALUES (?, ?, ?)
        """, (greeting.created_on, greeting.author, greeting.message))
        return True
