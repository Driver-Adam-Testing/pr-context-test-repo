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
