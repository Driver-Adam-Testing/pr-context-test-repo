"""Tests for priority management utilities."""

import pytest
from unittest.mock import MagicMock

from src.tasktracker.priorities import (
    Priority,
    get_priority_label,
    sort_by_priority,
    filter_by_priority,
    count_by_priority,
)


class TestPriority:
    """Tests for Priority enum."""

    def test_priority_ordering(self):
        """Priority values should be ordered correctly."""
        assert Priority.LOW < Priority.MEDIUM
        assert Priority.MEDIUM < Priority.HIGH
        assert Priority.HIGH < Priority.CRITICAL

    def test_priority_values(self):
        """Priority values should be integers 1-4."""
        assert Priority.LOW == 1
        assert Priority.MEDIUM == 2
        assert Priority.HIGH == 3
        assert Priority.CRITICAL == 4


class TestGetPriorityLabel:
    """Tests for get_priority_label function."""

    def test_returns_correct_labels(self):
        """Should return human-readable labels."""
        assert get_priority_label(Priority.LOW) == "Low"
        assert get_priority_label(Priority.MEDIUM) == "Medium"
        assert get_priority_label(Priority.HIGH) == "High"
        assert get_priority_label(Priority.CRITICAL) == "Critical"


class TestSortByPriority:
    """Tests for sort_by_priority function."""

    def test_sorts_descending_by_default(self):
        """Should sort highest priority first by default."""
        tasks = [
            MagicMock(priority=Priority.LOW),
            MagicMock(priority=Priority.CRITICAL),
            MagicMock(priority=Priority.MEDIUM),
        ]
        result = sort_by_priority(tasks)
        assert result[0].priority == Priority.CRITICAL
        assert result[1].priority == Priority.MEDIUM
        assert result[2].priority == Priority.LOW

    def test_sorts_ascending_when_specified(self):
        """Should sort lowest priority first when descending=False."""
        tasks = [
            MagicMock(priority=Priority.HIGH),
            MagicMock(priority=Priority.LOW),
        ]
        result = sort_by_priority(tasks, descending=False)
        assert result[0].priority == Priority.LOW
        assert result[1].priority == Priority.HIGH


class TestFilterByPriority:
    """Tests for filter_by_priority function."""

    def test_filters_below_minimum(self):
        """Should filter out tasks below minimum priority."""
        tasks = [
            MagicMock(priority=Priority.LOW),
            MagicMock(priority=Priority.HIGH),
            MagicMock(priority=Priority.CRITICAL),
        ]
        result = filter_by_priority(tasks, min_priority=Priority.HIGH)
        assert len(result) == 2
        assert all(t.priority >= Priority.HIGH for t in result)

    def test_includes_all_by_default(self):
        """Should include all tasks when min_priority is LOW."""
        tasks = [
            MagicMock(priority=Priority.LOW),
            MagicMock(priority=Priority.MEDIUM),
        ]
        result = filter_by_priority(tasks)
        assert len(result) == 2


class TestCountByPriority:
    """Tests for count_by_priority function."""

    def test_counts_correctly(self):
        """Should count tasks by priority level."""
        tasks = [
            MagicMock(priority=Priority.LOW),
            MagicMock(priority=Priority.LOW),
            MagicMock(priority=Priority.HIGH),
        ]
        counts = count_by_priority(tasks)
        assert counts[Priority.LOW] == 2
        assert counts[Priority.MEDIUM] == 0
        assert counts[Priority.HIGH] == 1
        assert counts[Priority.CRITICAL] == 0

    def test_empty_list(self):
        """Should return all zeros for empty list."""
        counts = count_by_priority([])
        assert all(count == 0 for count in counts.values())
