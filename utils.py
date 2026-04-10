"""
Script Name : utils.py
Description : Helper functions
Author      : @tonybnya
"""

from datetime import datetime, timezone


def current_timestamp() -> str:
    """Generate ISO 8601 UTC timestamp.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_name(name: str | None) -> tuple[bool, str | None]:
    """Validate name parameter.
    """
    if name is None:
        return False, "Missing 'name' query parameter"
    if not isinstance(name, str):
        return False, "Name must be a string"
    if not name.strip():
        return False, "Name cannot be empty"
    return True, None
