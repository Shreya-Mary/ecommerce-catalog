from util.db_connection import get_connection
from util.logger import logger  # ✅ Add logger import

class AuthService:
    def __init__(self) -> None:
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def authenticate(self, username: str, password: str) -> dict | None:
        try:
            query = "SELECT * FROM user WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()

            if result:
                logger.info("User '%s' authenticated successfully", username)
            else:
                logger.warning("Authentication failed for user '%s'", username)

            return result
        except Exception as e:
            logger.error("Error during authentication for user '%s': %s", username, str(e))
            return None

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            logger.error("Error closing DB connection in AuthService: %s", str(e))
