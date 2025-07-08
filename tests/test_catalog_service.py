import pytest
from dto.catalog import Catalog
from service.catalog_service import CatalogService

@pytest.fixture
def catalog_obj():
    return Catalog(
        "Test Catalog",
        "Test Description",
        "2025-07-01 10:00",
        "2025-07-05 18:00",
        "Active"
    )

# Test function for creating a catalog
def test_create_catalog(monkeypatch, catalog_obj):
    service = CatalogService()

    # Mock cursor with lastrowid
    class MockCursor:
        def __init__(self):
            self.lastrowid = 1

        def execute(self, query, params):
            pass

        def close(self):
            pass

    # Mock connection with commit
    class MockConnection:
        def commit(self):
            pass

        def close(self):
            pass

    # Inject mocks into the service
    service.cursor = MockCursor()
    service.conn = MockConnection()

    # Perform the create operation
    result = service.create_catalog(catalog_obj)

    # Assertions
    assert result["id"] == 1
    assert result["name"] == "Test Catalog"

def test_create_catalog(monkeypatch, catalog_obj):
    service = CatalogService()

    class MockCursor:
        def __init__(self):
            self.lastrowid = 1

        def execute(self, query, params):
            pass

        def close(self):
            pass

    class MockConnection:
        def commit(self):
            pass

        def close(self):
            pass

    # Inject mocks
    service.cursor = MockCursor()
    service.conn = MockConnection()

    result = service.create_catalog(catalog_obj)

    assert result["id"] == 1
    assert result["name"] == "Test Catalog"

def test_update_catalog(monkeypatch):
    service = CatalogService()

    # Mock execute and commit
    monkeypatch.setattr(service.cursor, "execute", lambda query, params: None)
    monkeypatch.setattr(service.conn, "commit", lambda: None)

    result = service.update_catalog_by_id(
        catalog_id=1,
        name="Updated",
        description="Updated Desc",
        start_date="2025-07-01 10:00",
        end_date="2025-07-05 18:00",
        status="Inactive"
    )
    assert result["message"] == "Catalog updated successfully"

def test_delete_catalog(monkeypatch):
    service = CatalogService()

    # Mock execute and commit
    monkeypatch.setattr(service.cursor, "execute", lambda query, params: None)
    monkeypatch.setattr(service.conn, "commit", lambda: None)

    result = service.delete_catalog_by_id(1)
    assert result["message"] == "Catalog deleted successfully"

