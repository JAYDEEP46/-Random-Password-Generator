"""
test_password_generator.py — Unit tests (Step 4: Test & Refine)
Run with:  python -m pytest test_password_generator.py -v
"""

import pytest
from core import generate_password, strength_score, CHAR_SETS


class TestGeneratePassword:

    def test_correct_length(self):
        pwd = generate_password(20, True, True, True, True)
        assert len(pwd) == 20

    def test_uppercase_only(self):
        pwd = generate_password(16, True, False, False, False)
        assert all(c in CHAR_SETS["uppercase"] for c in pwd)

    def test_lowercase_only(self):
        pwd = generate_password(16, False, True, False, False)
        assert all(c in CHAR_SETS["lowercase"] for c in pwd)

    def test_digits_only(self):
        pwd = generate_password(16, False, False, True, False)
        assert all(c in CHAR_SETS["digits"] for c in pwd)

    def test_symbols_only(self):
        pwd = generate_password(16, False, False, False, True)
        assert all(c in CHAR_SETS["symbols"] for c in pwd)

    def test_all_sets_included(self):
        """Password must contain at least one char from every selected set."""
        pwd = generate_password(32, True, True, True, True)
        assert any(c in CHAR_SETS["uppercase"] for c in pwd)
        assert any(c in CHAR_SETS["lowercase"] for c in pwd)
        assert any(c in CHAR_SETS["digits"]    for c in pwd)
        assert any(c in CHAR_SETS["symbols"]   for c in pwd)

    def test_exclude_characters(self):
        exclude = "0Ol1I"
        pwd = generate_password(50, True, True, True, False, exclude=exclude)
        assert not any(c in exclude for c in pwd)

    def test_no_charset_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            generate_password(16, False, False, False, False)

    def test_length_too_short_raises(self):
        """Length 1 can't satisfy 4 required chars (one from each set)."""
        with pytest.raises(ValueError):
            generate_password(1, True, True, True, True)

    def test_randomness(self):
        """Two passwords should (overwhelmingly) differ."""
        passwords = {generate_password(24, True, True, True, True) for _ in range(20)}
        assert len(passwords) > 1

    def test_minimum_length_boundary(self):
        pwd = generate_password(4, True, True, True, True)
        assert len(pwd) == 4


class TestStrengthScore:

    def test_short_no_variety_is_weak(self):
        _, label, _ = strength_score("abcdefg")
        assert label == "Weak"

    def test_long_mixed_is_strong(self):
        _, label, _ = strength_score("A1b!xYz9@qW#mN2&")
        assert label in ("Strong", "Very strong")

    def test_returns_color_hex(self):
        _, _, color = strength_score("Test1234!")
        assert color.startswith("#")

    def test_score_range(self):
        score, _, _ = strength_score("x")
        assert 0 <= score <= 6
