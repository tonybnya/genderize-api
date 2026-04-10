"""
Script Name : utils.py
Description : Helper functions
Author      : @tonybnya
"""
from datetime import datetime, timezone

def current_timestamp() -> str:
    """Generate ISO 8601 UTC timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
