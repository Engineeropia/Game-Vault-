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
