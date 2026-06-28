"""core.py — Pure password logic (no GUI dependencies)."""

import secrets
import string

CHAR_SETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "digits":    string.digits,
    "symbols":   "!@#$%^&*()-_=+[]{}|;:,.<>?",
}


def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude=""):
    pool = ""
    required = []

    for key, flag in [("uppercase", use_upper), ("lowercase", use_lower),
                      ("digits", use_digits), ("symbols", use_symbols)]:
        if flag:
            chars = "".join(c for c in CHAR_SETS[key] if c not in exclude)
            pool += chars
            if chars:
                required.append(secrets.choice(chars))

    if not pool:
        raise ValueError("Select at least one character set.")
    if length < len(required):
        raise ValueError(f"Length must be at least {len(required)} for chosen sets.")

    remaining = [secrets.choice(pool) for _ in range(length - len(required))]
    password_list = required + remaining
    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)


def strength_score(password):
    score = 0
    if len(password) >= 8:  score += 1
    if len(password) >= 16: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in CHAR_SETS["symbols"] for c in password): score += 1

    if score <= 2: return score, "Weak",        "#E24B4A"
    if score <= 3: return score, "Fair",        "#EF9F27"
    if score <= 4: return score, "Strong",      "#1D9E75"
    return score,          "Very strong", "#185FA5"
