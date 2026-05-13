import tkinter as tk
from tkinter import ttk, messagebox

# ─────────────────────────────────────────────
#  BACKEND
# ─────────────────────────────────────────────
PATH = "inventory.txt"

def initialize_file():
    open(PATH, "a").close()

def get_all_games():
    try:
        with open(PATH, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def add_game_logic(name, price, qua):
    with open(PATH, "a") as f:
        f.write(f"name:{name} | price:{price} | quantity:{qua}\n")

def sell_game_logic(game_name_to_sell):
    updated_lines = []
    found = False
    success = False
    try:
        with open(PATH, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return False, "File not found"

    for line in lines:
        parts = line.strip().split(" | ")
        if len(parts) < 3:
            continue
        n_file  = parts[0].split(":", 1)[1].strip()
        pr_file = parts[1].split(":", 1)[1].strip()
        q_file  = int(parts[2].split(":", 1)[1].strip())

        if n_file.lower() == game_name_to_sell.lower():
            found = True
            if q_file > 0:
                q_file -= 1
                success = True
            else:
                return False, "Out of stock"
        updated_lines.append(f"name:{n_file} | price:{pr_file} | quantity:{q_file}\n")

    with open(PATH, "w") as f:
        f.writelines(updated_lines)

    if not found:
        return False, "Game not found"
    return success, "Sold successfully"

def delete_game_logic(game_name_to_delete):
    try:
        with open(PATH, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return False, "File not found"

    new_lines = []
    found = False
    for line in lines:
parts = line.strip().split(" | ")
        if len(parts) >= 1:
            n_file = parts[0].split(":", 1)[1].strip()
            if n_file.lower() == game_name_to_delete.lower():
                found = True
                continue
        new_lines.append(line)

    if not found:
        return False, "Game not found"
    with open(PATH, "w") as f:
        f.writelines(new_lines)
    return True, "Deleted"

def calculate_total_logic():
    total = 0
    try:
        with open(PATH, "r") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 3:
                    price    = int(parts[1].split(":", 1)[1].strip())
                    quantity = int(parts[2].split(":", 1)[1].strip())
                    total += price * quantity
    except FileNotFoundError:
        pass
    return total

def parse_game_line(line):
    """Return (name, price, quantity) tuple or None."""
    parts = line.strip().split(" | ")
    if len(parts) < 3:
        return None
    try:
        name  = parts[0].split(":", 1)[1].strip()
        price = parts[1].split(":", 1)[1].strip()
        qty   = parts[2].split(":", 1)[1].strip()
        return name, price, qty
    except IndexError:
        return None


# ─────────────────────────────────────────────
#  THEME CONSTANTS  (dark gaming aesthetic)
# ─────────────────────────────────────────────
BG        = "#0d0d0f"
PANEL     = "#16161a"
CARD      = "#1e1e24"
ACCENT    = "#7f5af0"          # violet
ACCENT2   = "#2cb67d"          # teal-green  (success)
DANGER    = "#ef4565"          # red
TEXT      = "#fffffe"
SUBTEXT   = "#94a1b2"
BORDER    = "#2e2e3a"
FONT_H    = ("Courier New", 13, "bold")
FONT_BODY = ("Courier New", 11)
FONT_SM   = ("Courier New", 9)
FONT_LG   = ("Courier New", 16, "bold")
FONT_XL   = ("Courier New", 22, "bold")


# ─────────────────────────────────────────────
#  REUSABLE WIDGETS
# ─────────────────────────────────────────────
def styled_entry(parent, placeholder="", width=28):
    frame = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
