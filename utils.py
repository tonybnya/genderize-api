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
    if not any(c.isalpha() for c in name):
        return False, "Name must be a string"
    if not name.strip():
        return False, "Name cannot be empty"
    return True, None


def make_response(data: dict) -> tuple[dict | None, str | None]:
    """Process Genderize API response.
    """
    gender = data.get("gender")
    probability = data.get("probability")
    sample_size = data.get("count")

    # Edge case: null gender or zero count
    if gender is None or sample_size == 0:
        return None, "No prediction available for the provided name"

    # Compute confidence
    is_confident = probability >= 0.7 and sample_size >= 100

    return {
        "name": data.get("name"),
        "gender": gender,
        "probability": probability,
        "sample_size": sample_size,
        "is_confident": is_confident,
        "processed_at": current_timestamp(),
    }, None
