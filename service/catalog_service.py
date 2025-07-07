from util.db_connection import get_connection
from dto.catalog import Catalog
from util.logger import logger  # ✅ Added logging

class CatalogService:
    def __init__(self) -> None:
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def create_catalog(self, catalog: Catalog):
        try:
            self.cursor.execute(
                "INSERT INTO catalog (catalog_name, catalog_description, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)",
                (catalog.name, catalog.description, catalog.start_date, catalog.end_date, catalog.status)
            )
            self.conn.commit()
            inserted_id = self.cursor.lastrowid
            logger.info("Catalog created with ID %s", inserted_id)
            return {
                "id": inserted_id,
                "name": catalog.name,
                "description": catalog.description,
                "start_date": catalog.start_date,
                "end_date": catalog.end_date,
                "status": catalog.status
            }
        except Exception as e:
            logger.error("Error creating catalog: %s", str(e))
            return {"error": str(e)}

    def get_all_catalogs(self, status=None, sort_by="start_date", page=1, size=5, search=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM catalog"
        count_query = "SELECT COUNT(*) as total FROM catalog"
        conditions = []
        params = []

        if status:
            conditions.append("status = %s")
            params.append(status.capitalize())

        if search:
            conditions.append("(catalog_name LIKE %s OR catalog_id = %s)")
            params.append(f"%{search}%")
            try:
                params.append(int(search))
            except ValueError:
                params.append(-1)

        if conditions:
            condition_str = " WHERE " + " AND ".join(conditions)
            query += condition_str
            count_query += condition_str

        if sort_by == "start_date":
            query += " ORDER BY start_date DESC"
        else:
            query += " ORDER BY catalog_id DESC"

        offset = (page - 1) * size
        query += " LIMIT %s OFFSET %s"
        paginated_params = params + [size, offset]

        try:
            cursor.execute(query, tuple(paginated_params))
            result = cursor.fetchall()

            cursor.execute(count_query, tuple(params))
            total = cursor.fetchone()["total"]

            logger.info("Fetched catalogs (page=%s, size=%s, search=%s, status=%s)", page, size, search, status)
            return result, total
        except Exception as e:
            logger.error("Error fetching catalogs: %s", str(e))
            return [], 0
        finally:
            cursor.close()
            conn.close()

    def update_catalog_by_id(self, catalog_id: int, name: str, description: str, start_date: str, end_date: str, status: str) -> dict:
        try:
            self.cursor.execute(
                "UPDATE catalog SET catalog_name = %s, catalog_description = %s, start_date = %s, end_date = %s, status = %s WHERE catalog_id = %s",
                (name, description, start_date, end_date, status, catalog_id)
            )
            self.conn.commit()
            logger.info("Catalog %s updated", catalog_id)
            return {"message": "Catalog updated successfully"}
        except Exception as e:
            logger.error("Error updating catalog %s: %s", catalog_id, str(e))
            return {"error": str(e)}

    def delete_catalog_by_id(self, catalog_id: int) -> dict:
        try:
            self.cursor.execute("DELETE FROM catalog WHERE catalog_id = %s", (catalog_id,))
            self.conn.commit()
            logger.info("Catalog %s deleted", catalog_id)
            return {"message": "Catalog deleted successfully"}
        except Exception as e:
            logger.error("Error deleting catalog %s: %s", catalog_id, str(e))
            return {"error": str(e)}

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            logger.error("Error closing DB connection in destructor: %s", str(e))
