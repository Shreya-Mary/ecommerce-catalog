
from service.auth_service import AuthService

def test_authenticate_success(monkeypatch):
    service = AuthService()

    def mock_execute(query, params):
        service.cursor.fetchone = lambda: {"username": "admin"}

    monkeypatch.setattr(service.cursor, "execute", mock_execute)

    user = service.authenticate("admin", "admin123")
    assert user["username"] == "admin"

def test_authenticate_failure(monkeypatch):
    service = AuthService()

    def mock_execute(query, params):
        service.cursor.fetchone = lambda: None

    monkeypatch.setattr(service.cursor, "execute", mock_execute)

    user = service.authenticate("invalid", "wrong")
    assert user is None


