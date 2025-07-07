import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.catalog_service import CatalogService
from dto.catalog import Catalog

class MockCursor:
    def __init__(self):
        self.lastrowid = 1
    def execute(self, query, params):
        pass
    def close(self):
        pass
    def fetchall(self):
        return []
    def fetchone(self):
        return {"total": 0}

class MockConnection:
    def cursor(self, dictionary=True):
        return MockCursor()
    def commit(self):
        pass
    def close(self):
        pass

def test_create_catalog(monkeypatch):
    # Mock DB connection
    monkeypatch.setattr("service.catalog_service.get_connection", lambda: MockConnection())

    service = CatalogService()
    catalog = Catalog("Test Cat", "Test Desc", "2025-07-01 10:00", "2025-07-05 18:00", "Active")

    result = service.create_catalog(catalog)

    assert result["id"] == 1
    assert result["name"] == "Test Cat"


