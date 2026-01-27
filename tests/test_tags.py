"""Tests for tag management."""

import pytest
from src.tasktracker.tags import TagManager


class TestTagManager:
    """Tests for TagManager class."""

    def test_add_new_tag(self):
        """Adding a new tag returns True."""
        manager = TagManager()
        assert manager.add_tag("work") is True
        assert manager.has_tag("work")

    def test_add_duplicate_tag(self):
        """Adding a duplicate tag returns False."""
        manager = TagManager()
        manager.add_tag("work")
        assert manager.add_tag("work") is False

    def test_tag_normalization(self):
        """Tags are normalized to lowercase."""
        manager = TagManager()
        manager.add_tag("URGENT")
        assert manager.has_tag("urgent")
        assert manager.has_tag("URGENT")
        assert manager.has_tag("  urgent  ")

    def test_remove_existing_tag(self):
        """Removing an existing tag returns True."""
        manager = TagManager()
        manager.add_tag("temp")
        assert manager.remove_tag("temp") is True
        assert not manager.has_tag("temp")

    def test_remove_nonexistent_tag(self):
        """Removing a nonexistent tag returns False."""
        manager = TagManager()
        assert manager.remove_tag("missing") is False

    def test_get_all_tags_sorted(self):
        """get_all_tags returns sorted list."""
        manager = TagManager()
        manager.add_tag("zebra")
        manager.add_tag("alpha")
        manager.add_tag("beta")
        assert manager.get_all_tags() == ["alpha", "beta", "zebra"]

    def test_filter_valid(self):
        """filter_valid returns only existing tags."""
        manager = TagManager()
        manager.add_tag("work")
        manager.add_tag("home")
        result = manager.filter_valid(["work", "missing", "home", "unknown"])
        assert result == ["work", "home"]

    def test_count(self):
        """count returns number of tags."""
        manager = TagManager()
        assert manager.count() == 0
        manager.add_tag("a")
        manager.add_tag("b")
        assert manager.count() == 2

    def test_clear(self):
        """clear removes all tags."""
        manager = TagManager()
        manager.add_tag("a")
        manager.add_tag("b")
        manager.clear()
        assert manager.count() == 0
        assert manager.get_all_tags() == []

    def test_add_many(self):
        """add_many adds multiple tags and returns count of new ones."""
        manager = TagManager()
        manager.add_tag("existing")
        added = manager.add_many(["new1", "new2", "existing", "new3"])
        assert added == 3
        assert manager.count() == 4
