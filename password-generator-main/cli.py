"""
cli.py — Command-line interface for the password generator.

Usage examples:
    python cli.py
    python cli.py --length 24 --no-symbols
    python cli.py --length 32 --exclude "0Ol1I" --batch 5
"""

import argparse
from core import generate_password, strength_score


def parse_args():
    parser = argparse.ArgumentParser(
        description="Random Password Generator — secure, customisable"
    )
    parser.add_argument("--length",     type=int,  default=16,
                        help="Password length (default: 16)")
    parser.add_argument("--no-upper",   action="store_true",
                        help="Exclude uppercase letters")
    parser.add_argument("--no-lower",   action="store_true",
                        help="Exclude lowercase letters")
    parser.add_argument("--no-digits",  action="store_true",
                        help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Exclude symbols")
    parser.add_argument("--exclude",    type=str,  default="",
                        help="Specific characters to exclude (e.g. '0Ol1I')")
    parser.add_argument("--batch",      type=int,  default=1,
                        help="Number of passwords to generate (default: 1)")
    return parser.parse_args()


def color(text, hex_color):
    """Wrap text in ANSI color (best-effort; skipped on Windows cmd)."""
    try:
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
    except Exception:
        return text


def main():
    args = parse_args()

    print("\n🔐  Password Generator\n" + "─" * 40)

    for i in range(args.batch):
        try:
            pwd = generate_password(
                length      = args.length,
                use_upper   = not args.no_upper,
                use_lower   = not args.no_lower,
                use_digits  = not args.no_digits,
                use_symbols = not args.no_symbols,
                exclude     = args.exclude,
            )
            _, label, hex_col = strength_score(pwd)
            prefix = f"[{i+1}] " if args.batch > 1 else ""
            print(f"{prefix}{color(pwd, '#C9A84C')}  "
                  f"({color(label, hex_col)})")
        except ValueError as e:
            print(f"Error: {e}")
            break

    print("─" * 40 + "\n")


if __name__ == "__main__":
    main()
