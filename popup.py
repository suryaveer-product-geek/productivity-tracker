import tkinter as tk
from datetime import datetime
import threading
from tracker import save_entry

CATEGORIES = ["Productive", "Work", "Learning", "Personal", "Phone/Social", "Rest", "Sleep", "Exercise", "Meal"]

POPUP_TIMEOUT = 120

def show_popup(slot, timestamp):
    thread = threading.Thread(target=_create_popup, args=(slot, timestamp), daemon=True)
    thread.start()

def _create_popup(slot, timestamp):
    root = tk.Tk()
    root.withdraw()

    win = tk.Toplevel(root)
    win.title("Hourly Check-In")
    win.geometry("460x530")
    win.resizable(False, False)
    win.attributes("-topmost", True)
    win.attributes("-alpha", 0.0)

    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - 460) // 2
    y = (sh - 530) // 2
    win.geometry(f"460x530+{x}+{y}")

    # ── Light palette ───────────────────────────────────
    BG       = "#FFFEFB"
    ACCENT   = "#C9A87C"
    ACCENT2  = "#B8976B"
    TEXT     = "#2C2A27"
    SUBTEXT  = "#A8A49F"
    BORDER   = "#EDE9E3"
    ENTRY_BG = "#FAFAF8"
    ENTRY_FG = "#3A3632"
    SEL_BG   = "#FDF1E2"
    SEL_FG   = "#7A4E1A"
    BTN_FG   = "#FFFFFF"
    SLEEP_FG = "#A8A49F"

    win.configure(bg=BG)

    canvas = tk.Canvas(win, bg=BG, highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Top gold accent bar
    canvas.create_rectangle(0, 0, 460, 3, fill=ACCENT, outline="")
    # Outer border
    canvas.create_rectangle(0, 0, 459, 529, outline=BORDER, width=1)

    # ── Header ──────────────────────────────────────────
    header = tk.Frame(win, bg=BG)
    header.place(x=28, y=22, width=404)

    tk.Label(header, text="HOURLY CHECK-IN",
             font=("Courier New", 9, "bold"),
             fg=ACCENT, bg=BG).pack(anchor="w")

    tk.Label(header, text=slot,
             font=("Georgia", 27, "bold"),
             fg=TEXT, bg=BG).pack(anchor="w", pady=(3, 0))

    tk.Label(header, text=timestamp.strftime("%A, %d %B %Y"),
             font=("Courier New", 9),
             fg=SUBTEXT, bg=BG).pack(anchor="w")

    # Divider
    canvas.create_rectangle(28, 112, 432, 113, fill=BORDER, outline="")

    # ── Description label ───────────────────────────────
    tk.Label(win, text="What did you do this past hour?",
             font=("Georgia", 11), fg=SUBTEXT, bg=BG).place(x=28, y=126)

    # ── Text Entry ──────────────────────────────────────
    entry_frame = tk.Frame(win, bg=BORDER, padx=1, pady=1)
    entry_frame.place(x=28, y=150, width=404, height=86)

    entry_inner = tk.Frame(entry_frame, bg=ENTRY_BG)
    entry_inner.pack(fill="both", expand=True)

    desc_var = tk.Text(entry_inner, height=4,
                       font=("Georgia", 11),
                       fg=ENTRY_FG, bg=ENTRY_BG,
                       insertbackground=ACCENT,
                       relief="flat", padx=10, pady=8,
                       wrap="word")
    desc_var.pack(fill="both", expand=True)
    desc_var.focus_set()

    placeholder = "Describe your activity… leave blank to log as Sleep"
    desc_var.insert("1.0", placeholder)
    desc_var.config(fg=SUBTEXT)

    def on_focus_in(e):
        if desc_var.get("1.0", "end-1c") == placeholder:
            desc_var.delete("1.0", tk.END)
            desc_var.config(fg=ENTRY_FG)

    def on_focus_out(e):
        if not desc_var.get("1.0", "end-1c").strip():
            desc_var.insert("1.0", placeholder)
            desc_var.config(fg=SUBTEXT)

    desc_var.bind("<FocusIn>", on_focus_in)
    desc_var.bind("<FocusOut>", on_focus_out)

    # ── Category label ──────────────────────────────────
    tk.Label(win, text="How would you categorise it?",
             font=("Georgia", 11), fg=SUBTEXT, bg=BG).place(x=28, y=252)

    # ── Category Buttons ────────────────────────────────
    selected_cat = tk.StringVar(value="")
    cat_buttons = {}

    cat_frame = tk.Frame(win, bg=BG)
    cat_frame.place(x=28, y=276, width=404)

    def select_category(cat):
        selected_cat.set(cat)
        for c, btn in cat_buttons.items():
            if c == cat:
                btn.config(bg=SEL_BG, fg=SEL_FG,
                           highlightbackground=ACCENT, highlightthickness=1)
            else:
                btn.config(bg=BG, fg=SUBTEXT,
                           highlightbackground=BORDER, highlightthickness=1)

    row1 = tk.Frame(cat_frame, bg=BG)
    row1.pack(fill="x", pady=(0, 6))
    row2 = tk.Frame(cat_frame, bg=BG)
    row2.pack(fill="x")

    for cat in CATEGORIES[:5]:
        btn = tk.Button(row1, text=cat,
                        font=("Courier New", 8),
                        bg=BG, fg=SUBTEXT,
                        activebackground=SEL_BG, activeforeground=SEL_FG,
                        relief="flat",
                        highlightbackground=BORDER, highlightthickness=1,
                        padx=8, pady=5, cursor="hand2",
                        command=lambda c=cat: select_category(c))
        btn.pack(side="left", padx=(0, 5))
        cat_buttons[cat] = btn

    for cat in CATEGORIES[5:]:
        btn = tk.Button(row2, text=cat,
                        font=("Courier New", 8),
                        bg=BG, fg=SUBTEXT,
                        activebackground=SEL_BG, activeforeground=SEL_FG,
                        relief="flat",
                        highlightbackground=BORDER, highlightthickness=1,
                        padx=8, pady=5, cursor="hand2",
                        command=lambda c=cat: select_category(c))
        btn.pack(side="left", padx=(0, 5))
        cat_buttons[cat] = btn

    # ── Countdown ───────────────────────────────────────
    countdown_var = tk.StringVar(value="Auto-saving as Sleep in  2:00")
    tk.Label(win, textvariable=countdown_var,
             font=("Courier New", 9), fg=SUBTEXT, bg=BG).place(x=28, y=426)

    remaining = [POPUP_TIMEOUT]
    timer_active = [True]

    def tick():
        if not timer_active[0]:
            return
        remaining[0] -= 1
        if remaining[0] <= 0:
            countdown_var.set("Saving as Sleep...")
            auto_save()
        else:
            m = remaining[0] // 60
            s = remaining[0] % 60
            countdown_var.set(f"Auto-saving as Sleep in  {m}:{s:02d}")
            win.after(1000, tick)

    # ── Save logic ──────────────────────────────────────
    def do_save():
        timer_active[0] = False
        text = desc_var.get("1.0", "end-1c").strip()
        if text == placeholder:
            text = ""
        cat = selected_cat.get() or ("Sleep" if not text else "Productive")
        if not text:
            cat = "Sleep"
        save_entry(slot, text, cat, timestamp)
        fade_out()

    def auto_save():
        timer_active[0] = False
        save_entry(slot, "", "Sleep", timestamp)
        fade_out()

    # ── Buttons ─────────────────────────────────────────
    save_btn = tk.Button(win,
                         text="Save entry",
                         font=("Georgia", 11),
                         bg=ACCENT, fg=BTN_FG,
                         activebackground=ACCENT2, activeforeground=BTN_FG,
                         relief="flat", padx=20, pady=11,
                         cursor="hand2", command=do_save)
    save_btn.place(x=28, y=452, width=260, height=42)

    skip_btn = tk.Button(win,
                         text="Mark as Sleep",
                         font=("Courier New", 9),
                         bg=BG, fg=SLEEP_FG,
                         activebackground=BORDER, activeforeground=SUBTEXT,
                         relief="flat",
                         highlightbackground=BORDER, highlightthickness=1,
                         padx=10, pady=11,
                         cursor="hand2", command=auto_save)
    skip_btn.place(x=300, y=452, width=132, height=42)

    # ── Fade in / out ────────────────────────────────────
    def fade_in(alpha=0.0):
        alpha = min(alpha + 0.06, 1.0)
        win.attributes("-alpha", alpha)
        if alpha < 1.0:
            win.after(18, lambda: fade_in(alpha))

    def fade_out(alpha=1.0):
        alpha = max(alpha - 0.08, 0.0)
        win.attributes("-alpha", alpha)
        if alpha > 0:
            win.after(18, lambda: fade_out(alpha))
        else:
            win.destroy()
            root.destroy()

    win.deiconify()
    fade_in()
    win.after(1000, tick)
    root.mainloop()
