"""Tag management for tasks."""

from typing import List, Set


class TagManager:
    """Manages tags across all tasks."""

    def __init__(self):
        self._tags: Set[str] = set()

    def add_tag(self, tag: str) -> bool:
        """Add a tag to the global tag set.

        Returns True if tag was new, False if it already existed.
        """
        tag = self._normalize(tag)
        if tag in self._tags:
            return False
        self._tags.add(tag)
        return True

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the global set.

        Returns True if tag was removed, False if it didn't exist.
        """
        tag = self._normalize(tag)
        if tag not in self._tags:
            return False
        self._tags.discard(tag)
        return True

    def get_all_tags(self) -> List[str]:
        """Return all tags sorted alphabetically."""
        return sorted(self._tags)

    def has_tag(self, tag: str) -> bool:
        """Check if a tag exists."""
        return self._normalize(tag) in self._tags

    def _normalize(self, tag: str) -> str:
        """Normalize tag format: lowercase, strip whitespace."""
        return tag.lower().strip()

    def filter_valid(self, tags: List[str]) -> List[str]:
        """Filter a list of tags to only those that exist."""
        return [t for t in tags if self.has_tag(t)]

    def count(self) -> int:
        """Return the number of registered tags."""
        return len(self._tags)

    def clear(self) -> None:
        """Remove all tags."""
        self._tags.clear()

    def add_many(self, tags: List[str]) -> int:
        """Add multiple tags at once.

        Returns the number of new tags added.
        """
        added = 0
        for tag in tags:
            if self.add_tag(tag):
                added += 1
        return added
