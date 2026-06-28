# 🔐 Random Password Generator

A Python project built in two modes — a **GUI desktop app** (Tkinter) and a **command-line tool** — that generates cryptographically secure passwords with full customisation.

---

## Features

- Cryptographically secure randomness via Python's `secrets` module
- Choose character sets: uppercase, lowercase, digits, symbols
- Exclude specific characters (e.g. ambiguous `0Ol1I`)
- Live password strength meter (Weak → Very Strong)
- One-click clipboard copy
- Batch generation (5 passwords at once)
- CLI mode with flags for scripting and automation

---

## Project Structure

```
password_generator/
├── password_generator.py      # Core logic + GUI app
├── cli.py                     # Command-line interface
├── test_password_generator.py # Unit tests (pytest)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/password_generator.git
cd password_generator
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the GUI

```bash
python password_generator.py
```

The GUI launches with a password already generated. Use the sliders, checkboxes, and exclude field to customise, then click **Generate** or **Batch (5)**.

---

## Run the CLI

```bash
# Default: 16-char password with all character sets
python cli.py

# Custom length
python cli.py --length 32

# No symbols
python cli.py --length 24 --no-symbols

# Exclude ambiguous characters
python cli.py --exclude "0Ol1I"

# Generate 5 passwords
python cli.py --batch 5

# All options together
python cli.py --length 20 --no-symbols --exclude "0Ol1I" --batch 3
```

### CLI flags

| Flag | Default | Description |
|------|---------|-------------|
| `--length N` | 16 | Password length |
| `--no-upper` | off | Exclude uppercase A-Z |
| `--no-lower` | off | Exclude lowercase a-z |
| `--no-digits` | off | Exclude digits 0-9 |
| `--no-symbols` | off | Exclude symbols |
| `--exclude "chars"` | "" | Specific chars to exclude |
| `--batch N` | 1 | Number of passwords |

---

## Run Tests

```bash
python -m pytest test_password_generator.py -v
```

All 12 tests cover: length accuracy, character set inclusion, exclusion logic, error handling, randomness, and strength scoring.

---

## Security Notes

- Uses Python's `secrets` module — cryptographically secure, suitable for passwords
- Does **not** use `random` (which is not cryptographically secure)
- Passwords are never stored or logged

---

## Workflow (how this was built)

| Step | Action |
|------|--------|
| 1 | Reviewed project requirements (GUI + CLI, security rules, clipboard) |
| 2 | Designed architecture: core logic separate from UI |
| 3 | Developed `password_generator.py` (core + GUI) and `cli.py` |
| 4 | Tested with pytest — edge cases, exclusions, strength scoring |
| 5 | Added README, `.gitignore`, `requirements.txt` — pushed to GitHub |

---

## License

MIT — free to use, modify, and distribute.
