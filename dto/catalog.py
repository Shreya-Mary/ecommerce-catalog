class Catalog:
    def __init__(self, catalog_name: str, catalog_description: str, start_date: str, end_date: str, status: str = 'Active') -> None:
        self.name = catalog_name
        self.description = catalog_description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
