import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from app.core.utils import value_matches


@pytest.mark.parametrize(
    "a, b, match_all_in_list, expected",
    [
        # String vs String
        ("foo", "foo", False, True),
        ("foo", "bar", False, False),
        ("foo", "Foo", False, False),  # Case-sensitive
        ("", "", False, True),
        ("", None, False, False),
        (None, "", False, False),
        (None, None, False, False),
        # String vs List
        ("foo", ["foo", "bar"], False, True),
        ("bar", ["foo", "bar"], False, True),
        ("baz", ["foo", "bar"], False, False),
        ("foo", [], False, False),
        ("", [""], False, True),
        ("", [None], False, False),
        # List vs String
        (["foo", "bar"], "foo", False, True),
        (["foo", "bar"], "bar", False, True),
        (["foo", "bar"], "baz", False, False),
        ([], "foo", False, False),
        ([""], "", False, True),
        ([None], "", False, False),
        # List vs List (match_all_in_list=False)
        (["foo", "bar"], ["bar", "foo"], False, True),
        (["foo", "bar"], ["baz", "qux"], False, False),
        (["foo", "bar"], ["bar", "baz"], False, True),
        (["foo", "bar"], [], False, False),
        ([], ["foo", "bar"], False, False),
        # List vs List (match_all_in_list=True)
        (["foo", "bar"], ["bar", "foo"], True, True),
        (["foo", "bar"], ["foo", "bar"], True, True),
        (["foo", "bar"], ["foo"], True, False),
        (["foo"], ["foo", "bar"], True, False),
        (["foo", "bar"], ["bar", "baz"], True, False),
        (["foo", "bar"], [], True, False),
        ([], ["foo", "bar"], True, False),
        ([], [], True, True),
        # Typmischungen
        ("foo", None, False, False),
        (None, "foo", False, False),
        ([None], None, False, False),
        (None, [None], False, False),
        # Listen mit gemischten Typen
        (["1", 1], [1, "1"], True, True),
        (["foo", 1], [1, "foo"], True, True),
        (["foo", 1], [1, "bar"], False, True),
        (["foo", 1], [2, "bar"], False, False),
    ],
)
def test_value_matches_exhaustive(a, b, match_all_in_list, expected):
    assert value_matches(a, b, match_all_in_list) == expected


def test_value_matches_match_all_checkbox_behavior():
    # Mindestens ein Element muss matchen (default)
    assert value_matches(["foo", "bar"], ["bar", "baz"]) is True
    assert value_matches(["foo", "bar"], ["baz", "qux"]) is False
    assert value_matches(["foo", "bar"], ["foo", "bar", "baz"]) is True
    # Alle Elemente müssen matchen
    assert value_matches(["foo", "bar"], ["bar", "foo"], match_all_in_list=True) is True
    assert value_matches(["foo", "bar"], ["foo", "bar"], match_all_in_list=True) is True
    assert value_matches(["foo", "bar"], ["foo"], match_all_in_list=True) is False
    assert value_matches(["foo"], ["foo", "bar"], match_all_in_list=True) is False
    assert (
        value_matches(["foo", "bar"], ["bar", "baz"], match_all_in_list=True) is False
    )
    assert value_matches(["foo", "bar"], [], match_all_in_list=True) is False
    assert value_matches([], ["foo", "bar"], match_all_in_list=True) is False
    assert value_matches([], [], match_all_in_list=True) is True
    # String vs. Liste, beide Modi
    assert value_matches("foo", ["foo", "bar"], match_all_in_list=False) is True
    assert value_matches("foo", ["foo", "bar"], match_all_in_list=True) is False
    assert value_matches(["foo", "bar"], "foo", match_all_in_list=False) is True
    assert value_matches(["foo", "bar"], "foo", match_all_in_list=True) is False
    # Typmischungen
    assert value_matches([1, "foo"], ["foo", 1], match_all_in_list=True) is True
    assert value_matches([1, "foo"], ["foo", 2], match_all_in_list=True) is False
    assert value_matches([1, "foo"], ["foo", 2], match_all_in_list=False) is True
    assert value_matches([1, "foo"], [2, "bar"], match_all_in_list=False) is False
