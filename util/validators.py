from datetime import datetime
from exception.catalog_custom_exception import ValidationError


def validate_name(name:str)  ->None:
    """
    Checks if the catalog name is not empty.

    Args:
        name (str): The name of the catalog.

    Raises:
        ValidationError: If the name is empty or only spaces.
    """
    if not name.strip():
        raise ValidationError("Catalog name cannot be empty.")

def validate_description(description:str)  ->None:
     """
    Checks if the catalog description is not empty.

    Args:
        description (str): The description of the catalog.

    Raises:
        ValidationError: If the description is empty or only spaces.
    """
     if not description.strip():
        raise ValidationError("Catalog description cannot be empty.")

def validate_date_format(date_str:str, label:str)  -> datetime:
    """
    Validates the format of a date string.

    Args:
        date_str (str): The date to check.
        label (str): A label like 'Start date' or 'End date'.

    Returns:
        datetime: A datetime object if valid.

    Raises:
        ValidationError: If the date format is incorrect.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValidationError(f"{label} must be in YYYY-MM-DD HH:MM:SS format.")

def validate_date_order(start:str, end:str)  ->None:
     """
    Validates that end date is after the start date.

    Args:
        start (str): Start date string.
        end (str): End date string.

    Raises:
        ValidationError: If end date is before start date.
    """
     start_dt = validate_date_format(start, "Start date")
     end_dt = validate_date_format(end, "End date")
     if end_dt < start_dt:
        raise ValidationError("End date cannot be before start date.")

def validate_catalog_data(name :str, description :str, start :str, end :str)  ->None:
    """
    Validates all catalog input fields.

    Args:
        name (str): Catalog name.
        description (str): Catalog description.
        start (str): Start date.
        end (str): End date.

    Raises:
        ValidationError: If any field is invalid.
    """
    validate_name(name)
    validate_description(description)
    validate_date_order(start, end)

def validate_catalog_id(catalog_id: int)  ->None:
    """
    Validates that catalog ID is a positive integer.

    Args:
        catalog_id (int): Catalog ID to check.

    Raises:
        ValidationError: If ID is not a positive number.
    """
    if not isinstance(catalog_id, int) or catalog_id <= 0:
        raise ValidationError("Catalog ID must be a positive number.")