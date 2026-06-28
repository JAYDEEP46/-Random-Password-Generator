import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import pyperclip
from core import generate_password, strength_score  



# ── GUI ───────────────────────────────────────────────────────────────────────

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)
        self.configure(bg="#1a1a2e", padx=24, pady=24)

        self._build_ui()
        self._generate()          # show a password on launch

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        GOLD   = "#C9A84C"
        BG     = "#1a1a2e"
        CARD   = "#16213e"
        FG     = "#f0f0f0"
        MUTED  = "#888799"
        FONT   = ("Helvetica Neue", 11)
        HFONT  = ("Helvetica Neue", 20, "bold")

        # Title
        tk.Label(self, text="🔐 Password Generator", font=HFONT,
                 bg=BG, fg=GOLD).pack(pady=(0, 4))
        tk.Label(self, text="Cryptographically secure  ·  Fully customisable",
                 font=FONT, bg=BG, fg=MUTED).pack(pady=(0, 18))

        # ── Output card ───────────────────────────────────────────────────────
        out_frame = tk.Frame(self, bg=CARD, padx=14, pady=12,
                             highlightbackground=GOLD,
                             highlightthickness=1)
        out_frame.pack(fill="x", pady=(0, 8))

        self.pass_var = tk.StringVar()
        tk.Entry(out_frame, textvariable=self.pass_var,
                 font=("Courier New", 14), bg=CARD, fg=FG,
                 relief="flat", state="readonly",
                 readonlybackground=CARD,
                 width=34).pack(side="left")

        tk.Button(out_frame, text="Copy", font=FONT,
                  bg=GOLD, fg="#1a1a2e", relief="flat",
                  padx=10, cursor="hand2",
                  command=self._copy).pack(side="right")

        # Strength bar
        self.strength_label = tk.Label(self, text="", font=FONT,
                                       bg=BG, fg=FG, anchor="w")
        self.strength_label.pack(fill="x", pady=(0, 2))

        self.strength_bar = ttk.Progressbar(self, length=400,
                                            mode="determinate",
                                            maximum=6)
        self.strength_bar.pack(fill="x", pady=(0, 14))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TProgressbar", troughcolor=CARD,
                        background=GOLD, thickness=6)

        # ── Length slider ─────────────────────────────────────────────────────
        len_row = tk.Frame(self, bg=BG)
        len_row.pack(fill="x", pady=(0, 12))
        tk.Label(len_row, text="Length", font=FONT, bg=BG,
                 fg=MUTED, width=10, anchor="w").pack(side="left")
        self.len_var = tk.IntVar(value=16)
        tk.Scale(len_row, from_=6, to=64, orient="horizontal",
                 variable=self.len_var, bg=BG, fg=FG,
                 highlightthickness=0, troughcolor=CARD,
                 activebackground=GOLD, font=FONT,
                 command=lambda _: self._generate()).pack(side="left", fill="x", expand=True)
        self.len_display = tk.Label(len_row, textvariable=self.len_var,
                                    font=("Courier New", 12, "bold"),
                                    bg=BG, fg=GOLD, width=3)
        self.len_display.pack(side="left")

        # ── Checkboxes ────────────────────────────────────────────────────────
        check_frame = tk.Frame(self, bg=BG)
        check_frame.pack(fill="x", pady=(0, 12))

        self.use_upper   = self._checkbox(check_frame, "Uppercase  A-Z",   True,  0)
        self.use_lower   = self._checkbox(check_frame, "Lowercase  a-z",   True,  1)
        self.use_digits  = self._checkbox(check_frame, "Numbers    0-9",   True,  2)
        self.use_symbols = self._checkbox(check_frame, "Symbols  !@#…",    True,  3)

        # ── Exclude field ─────────────────────────────────────────────────────
        excl_frame = tk.Frame(self, bg=BG)
        excl_frame.pack(fill="x", pady=(0, 18))
        tk.Label(excl_frame, text="Exclude chars", font=FONT,
                 bg=BG, fg=MUTED, anchor="w", width=14).pack(side="left")
        self.excl_var = tk.StringVar()
        tk.Entry(excl_frame, textvariable=self.excl_var,
                 font=("Courier New", 11), bg=CARD, fg=FG,
                 insertbackground=FG, relief="flat",
                 width=28).pack(side="left", fill="x", expand=True)
        self.excl_var.trace_add("write", lambda *_: self._generate())

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(fill="x", pady=(0, 14))

        tk.Button(btn_frame, text="Generate",
                  font=("Helvetica Neue", 12, "bold"),
                  bg=GOLD, fg="#1a1a2e", relief="flat",
                  padx=20, pady=8, cursor="hand2",
                  command=self._generate).pack(side="left", fill="x",
                                               expand=True, padx=(0, 8))

        tk.Button(btn_frame, text="Batch (5)",
                  font=FONT, bg=CARD, fg=FG,
                  relief="flat", padx=12, pady=8, cursor="hand2",
                  command=self._batch).pack(side="left")

        # ── Batch output ──────────────────────────────────────────────────────
        self.batch_frame = tk.Frame(self, bg=BG)
        self.batch_frame.pack(fill="x")

    def _checkbox(self, parent, label, default, col):
        var = tk.BooleanVar(value=default)
        tk.Checkbutton(parent, text=label, variable=var,
                       font=("Courier New", 10),
                       bg="#1a1a2e", fg="#f0f0f0",
                       selectcolor="#16213e",
                       activebackground="#1a1a2e",
                       activeforeground="#C9A84C",
                       command=self._generate).grid(
                           row=0, column=col, padx=8, sticky="w")
        return var

    # ── Actions ───────────────────────────────────────────────────────────────

    def _generate(self):
        try:
            pwd = generate_password(
                length      = self.len_var.get(),
                use_upper   = self.use_upper.get(),
                use_lower   = self.use_lower.get(),
                use_digits  = self.use_digits.get(),
                use_symbols = self.use_symbols.get(),
                exclude     = self.excl_var.get(),
            )
            self.pass_var.set(pwd)
            score, label, color = strength_score(pwd)
            self.strength_label.config(text=f"Strength: {label}", fg=color)
            self.strength_bar["value"] = score
        except ValueError as e:
            self.pass_var.set("")
            self.strength_label.config(text=str(e), fg="#E24B4A")
            self.strength_bar["value"] = 0

    def _copy(self):
        pwd = self.pass_var.get()
        if not pwd:
            return
        try:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        except Exception:
            self.clipboard_clear()
            self.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

    def _batch(self):
        for widget in self.batch_frame.winfo_children():
            widget.destroy()

        try:
            passwords = [generate_password(
                length      = self.len_var.get(),
                use_upper   = self.use_upper.get(),
                use_lower   = self.use_lower.get(),
                use_digits  = self.use_digits.get(),
                use_symbols = self.use_symbols.get(),
                exclude     = self.excl_var.get(),
            ) for _ in range(5)]
        except ValueError as e:
            tk.Label(self.batch_frame, text=str(e),
                     fg="#E24B4A", bg="#1a1a2e",
                     font=("Helvetica Neue", 10)).pack()
            return

        tk.Label(self.batch_frame, text="5 passwords",
                 font=("Helvetica Neue", 10),
                 bg="#1a1a2e", fg="#888799").pack(anchor="w", pady=(8, 4))

        for pwd in passwords:
            row = tk.Frame(self.batch_frame, bg="#16213e",
                           padx=10, pady=6,
                           highlightbackground="#2a2a4a",
                           highlightthickness=1)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=pwd, font=("Courier New", 10),
                     bg="#16213e", fg="#f0f0f0").pack(side="left")

            p = pwd   # capture for lambda
            tk.Button(row, text="Copy", font=("Helvetica Neue", 9),
                      bg="#C9A84C", fg="#1a1a2e", relief="flat",
                      padx=6, cursor="hand2",
                      command=lambda x=p: pyperclip.copy(x)).pack(side="right")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
