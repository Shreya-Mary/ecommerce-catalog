
from dto.catalog import Catalog
from service.catalog_service import CatalogService

def test_create_catalog(monkeypatch):
    service = CatalogService()

    catalog = Catalog(
        name="Test Catalog",
        description="Test Description",
        start_date="2025-07-01 10:00",
        end_date="2025-07-05 18:00",
        status="Active"
    )

    # Mock cursor.execute to simulate DB insert
    def mock_execute(query, params):
        pass  # do nothing

    # Mock connection commit
    def mock_commit():
        pass

    # Mock lastrowid manually
    service.cursor.execute = mock_execute
    service.conn.commit = mock_commit
    service.cursor.lastrowid = 1

    result = service.create_catalog(catalog)
    assert result["id"] == 1
    assert result["name"] == "Test Catalog"




