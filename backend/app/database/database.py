import psycopg2
from psycopg2.extras import RealDictCursor

from app.config.config import config


class Database:
    def __init__(self):
        """Initialize the database connection as None."""
        self.conn = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                config.DATABASE_URL, cursor_factory=RealDictCursor
            )
            self.conn.autocommit = (
                True  # ✅ Enable autocommit to prevent connection locks
            )
            self.create_users_table()
            return self.conn
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return None

    def is_connected(self):
        """Check if the database connection is active and return it."""
        if self.conn is None or self.conn.closed:
            self.conn = self.connect()  #  Reconnect if closed

        return self.conn if self.conn else None

    def create_users_table(self):
        """Create the users table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            username VARCHAR(80) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
        if self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
