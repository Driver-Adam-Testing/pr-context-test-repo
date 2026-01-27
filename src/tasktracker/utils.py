"""Utility functions for TaskTracker."""

from datetime import datetime


def format_timestamp(dt: datetime) -> str:
    """Format a datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M")


def truncate_string(s: str, max_length: int = 50) -> str:
    """Truncate a string to max_length, adding ellipsis if needed."""
    if len(s) <= max_length:
        return s
    return s[: max_length - 3] + "..."


def time_ago(dt: datetime) -> str:
    """Return a human-readable time ago string."""
    now = datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


def filter_by_keyword(items: list, keyword: str, field: str = "title") -> list:
    """Filter a list of items by keyword match on a field."""
    keyword_lower = keyword.lower()
    return [item for item in items if keyword_lower in getattr(item, field, "").lower()]
