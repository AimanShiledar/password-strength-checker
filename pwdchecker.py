import re
import sys

# ─────────────────────────────────────────────
#  ANSI colour helpers
# ─────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"

def colored(text, *codes):
    return "".join(codes) + text + RESET


# ─────────────────────────────────────────────
#  Core checker
# ─────────────────────────────────────────────
def check_password(password: str) -> dict:
    rules = {
        "length_8":    (len(password) >= 8,  "At least 8 characters"),
        "length_12":   (len(password) >= 12, "12+ characters (great length)"),
        "uppercase":   (bool(re.search(r"[A-Z]", password)), "Uppercase letter (A–Z)"),
        "lowercase":   (bool(re.search(r"[a-z]", password)), "Lowercase letter (a–z)"),
        "digit":       (bool(re.search(r"\d",   password)), "Number (0–9)"),
        "special":     (bool(re.search(r"[^A-Za-z0-9]", password)), "Special character (!@#$…)"),
    }

    # Score based on core rules (excluding bonus length)
    core_rules = ["length_8", "uppercase", "lowercase", "digit", "special"]
    passed_core = sum(1 for k in core_rules if rules[k][0])

    if len(password) == 0:
        score, level, colour = 0, "—", GRAY
    elif passed_core <= 2:
        score, level, colour = 1, "Weak", RED
    elif passed_core == 3:
        score, level, colour = 2, "Fair", YELLOW
    elif passed_core == 4:
        score, level, colour = 3, "Strong", BLUE
    else:
        score, level, colour = 4, "Very Strong", GREEN

    tips = {
        0: "Start typing a password.",
        1: "Add uppercase letters, numbers, and symbols to strengthen it.",
        2: "Try making it longer or adding a special character.",
        3: "Almost there — a few more characters would make it very strong!",
        4: "Excellent password! Keep it safe.",
    }

    return {
        "score":   score,
        "max":     4,
        "level":   level,
        "colour":  colour,
        "rules":   rules,
        "tip":     tips[score],
        "length":  len(password),
    }


# ─────────────────────────────────────────────
#  Display helpers
# ─────────────────────────────────────────────
BAR_CHARS = ("▱", "▰")          # empty / filled

def strength_bar(score: int, max_score: int = 4, width: int = 20) -> str:
    filled     = round((score / max_score) * width)
    colours    = [RED, YELLOW, BLUE, GREEN]
    bar_colour = colours[score - 1] if score > 0 else GRAY
    bar        = colored(BAR_CHARS[1] * filled, bar_colour)
    bar       += colored(BAR_CHARS[0] * (width - filled), GRAY)
    return bar


def rule_line(passed: bool, label: str) -> str:
    icon   = colored("✔", GREEN, BOLD) if passed else colored("○", GRAY)
    text   = colored(label, WHITE) if passed else colored(label, GRAY)
    return f"  {icon}  {text}"


def print_result(password: str, result: dict) -> None:
    score   = result["score"]
    level   = result["level"]
    colour  = result["colour"]
    length  = result["length"]

    print()
    print(colored("  ┌─ Password Strength Checker ─────────────────────┐", GRAY))
    print()

    # Masked password preview
    masked = ("•" * min(length, 20)) + ("…" if length > 20 else "")
    print(f"  {colored('Password:', DIM + WHITE)}  {colored(masked, CYAN)}  "
          f"{colored(f'({length} chars)', GRAY)}")
    print()

    # Strength bar
    bar = strength_bar(score) if score > 0 else colored(BAR_CHARS[0] * 20, GRAY)
    print(f"  {bar}  {colored(f'{score}/4', GRAY)}  {colored(level, colour + BOLD)}")
    print()

    # Checklist
    print(colored("  Rules", DIM + WHITE))
    for key, (passed, label) in result["rules"].items():
        print(rule_line(passed, label))

    print()

    # Tip
    print(f"  {colored('Tip:', BOLD + WHITE)} {colored(result['tip'], GRAY)}")
    print()
    print(colored("  └──────────────────────────────────────────────────┘", GRAY))
    print()


# ─────────────────────────────────────────────
#  Interactive loop
# ─────────────────────────────────────────────
def interactive_mode() -> None:
    print()
    print(colored("  Password Strength Checker", BOLD + CYAN))
    print(colored("  Type a password and press Enter. Type 'quit' to exit.", GRAY))

    while True:
        try:
            print()
            password = input(colored("  Enter password: ", WHITE))
        except (EOFError, KeyboardInterrupt):
            print(colored("\n\n  Goodbye!\n", GRAY))
            break

        if password.lower() in ("quit", "exit", "q"):
            print(colored("\n  Goodbye!\n", GRAY))
            break

        result = check_password(password)
        print_result(password, result)


# ─────────────────────────────────────────────
#  CLI — check a password passed as argument
# ─────────────────────────────────────────────
def cli_mode(password: str) -> None:
    result = check_password(password)
    print_result(password, result)
    sys.exit(0 if result["score"] >= 3 else 1)


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode(sys.argv[1])
    else:
        interactive_mode()