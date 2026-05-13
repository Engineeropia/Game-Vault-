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
e = tk.Entry(
        frame, width=width, bg=CARD, fg=TEXT,
        insertbackground=ACCENT, relief="flat",
        font=FONT_BODY, bd=6,
        highlightthickness=0,
    )
    e.pack()

    def _add_placeholder():
        if not e.get():
            e.insert(0, placeholder)
            e.config(fg=SUBTEXT)

    def _clear_placeholder(event):
        if e.get() == placeholder:
            e.delete(0, tk.END)
            e.config(fg=TEXT)

    def _restore_placeholder(event):
        if not e.get():
            e.insert(0, placeholder)
            e.config(fg=SUBTEXT)

    e.bind("<FocusIn>",  _clear_placeholder)
    e.bind("<FocusOut>", _restore_placeholder)
    _add_placeholder()

    # Store placeholder text for later validation
    e._placeholder = placeholder

    def get_real():
        val = e.get()
        return "" if val == placeholder else val

    e.get_real = get_real
    return frame, e


def icon_button(parent, text, command, color=ACCENT, width=18):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=TEXT, activebackground=color,
        activeforeground=TEXT, font=FONT_H,
        relief="flat", bd=0, padx=14, pady=8,
        cursor="hand2", width=width,
    )
    # Hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=_lighten(color)))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def _lighten(hex_color):
    """Return a slightly lighter shade."""
    h = hex_color.lstrip("#")
    rgb = tuple(min(255, int(h[i:i+2], 16) + 30) for i in (0, 2, 4))
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def section_label(parent, text):
    tk.Label(
        parent, text=text, bg=PANEL, fg=ACCENT,
        font=FONT_H, anchor="w",
    ).pack(fill="x", padx=20, pady=(18, 4))
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=20)


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
class GameInventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        initialize_file()
        self.title("GAME VAULT  —  Inventory Manager")
        self.geometry("1050x680")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._build_layout()
        self.refresh_table()

    # ── Layout skeleton ──────────────────────
    def _build_layout(self):
        # ── TOP BAR ──
        topbar = tk.Frame(self, bg=PANEL, height=56)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(
            topbar, text="◈  GAME VAULT", bg=PANEL, fg=ACCENT,
            font=FONT_XL,
        ).pack(side="left", padx=24, pady=10)

        self.total_var = tk.StringVar(value="Portfolio Value: $0")
        tk.Label(
            topbar, textvariable=self.total_var, bg=PANEL, fg=ACCENT2,
            font=FONT_H,
        ).pack(side="right", padx=24)

        # ── MAIN BODY (sidebar + content) ──
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg=PANEL, width=300)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        content = tk.Frame(body, bg=BG)
        content.pack(side="left", fill="both", expand=True, padx=16, pady=16)

        self._build_sidebar(sidebar)
        self._build_table(content)

          # ── STATUS BAR ──
        self.status_var = tk.StringVar(value="Ready.")
        statusbar = tk.Frame(self, bg=CARD, height=28)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)
        tk.Label(
            statusbar, textvariable=self.status_var,
            bg=CARD, fg=SUBTEXT, font=FONT_SM, anchor="w",
        ).pack(side="left", padx=12, pady=4)

    # ── Sidebar ──────────────────────────────
    def _build_sidebar(self, parent):
        tk.Label(
            parent, text="OPERATIONS", bg=PANEL, fg=SUBTEXT,
            font=FONT_SM,
        ).pack(anchor="w", padx=20, pady=(20, 4))
