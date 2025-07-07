import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.auth_service import AuthService

def test_valid_login(monkeypatch):
    service = AuthService()

    def mock_execute(query, params):
        service.cursor.fetchone = lambda: {"username": "admin", "password": "admin123"}

    monkeypatch.setattr(service.cursor, "execute", mock_execute)

    result = service.authenticate("admin", "admin123")
    assert result is not None
    assert result["username"] == "admin"

