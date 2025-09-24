import sys, re, tkinter as tk
from tkinter import ttk, messagebox, font, Toplevel
from datetime import date, datetime
from ui.theme import apply_theme, THEMES
from ui.widgets import Card, GlowTile, NavBar, PillButton
from ui.i18n import i18n
from screens.settings import SettingsPopup
from ui.calendar import open_calendar_popup

try:
    import winsound
except Exception:
    winsound = None

USER_NAME = "Human"  


class TodoScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="App.TFrame", padding=16)
        self.master = master
        self.pack(fill="both", expand=True)
        
        # --- Fonts ---
        self.f_header = font.Font(family="Segoe UI", size=14, weight="bold")
        self.f_small = font.Font(family="Segoe UI", size=9)
        self.tasks_font = font.Font(family="Segoe UI", size=11, weight="bold")

        # --- Model + State ---
        self.tasks_data = []
        self._selected_due_date_obj = None
        self.var_timer_mins = tk.StringVar(value="25")
        self.timer_seconds = 25 * 60
        self.timer_running = False
        self.timer_job = None

        self._build_home()
        self._start_due_check()

    # ---------- basics ----------
    def _clear(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        for w in self.winfo_children():
            w.destroy()

    def _rebuild_all(self):
        """Destroys and rebuilds the entire UI to apply theme and language changes."""
        self.destroy()
        apply_theme(self.master, i18n.theme)
        TodoScreen(self.master)

    # ---------- home ----------
    def _build_home(self):
        self._clear()

        head = Card(self, w=700, h=110, title=i18n.t("hello_name", name=USER_NAME),
                    subtitle=i18n.t("welcome"), tag="🏠")
        head.pack(pady=(0, 12))

        row = ttk.Frame(self, style="App.TFrame")
        row.pack(pady=6)
        GlowTile(row, i18n.t("add"), "+", "accent2", command=self._add_popup).pack(side="left", padx=8)
        GlowTile(row, i18n.t("today"), date.today().strftime("%d %b"), "accent").pack(side="left", padx=8)

        list_card = Card(self, w=700, h=350, title=i18n.t("tasks"), tag=i18n.t("list"))
        list_card.pack(pady=10)
        self._build_tasks(list_card.inner)

        NavBar(self, on_home=self._build_home, on_add=self._add_popup,
               on_settings=self._open_settings, on_timer=self._build_timer).pack(pady=8)

    # ---------- timer screen ----------
    def _get_timer_duration_seconds(self):
        try:
            val = self.var_timer_mins.get()
            if not val: return 25 * 60
            mins = int(val)
            return max(1, mins) * 60
        except (ValueError, tk.TclError):
            return 25 * 60

    def _build_timer(self):
        self._clear()
        self.timer_running = False

        top = Card(self, w=700, h=420, title=i18n.t("pomodoro"), tag="⏱️")
        top.pack(pady=8)
        box = ttk.Frame(top.inner, style="Card.TFrame")
        box.pack(fill="both", expand=True, pady=10)

        self.timer_label = ttk.Label(box, text="25:00", font=("Segoe UI", 88, "bold"), style="Card.TLabel")
        self.timer_label.pack(pady=10)

        settings_frame = ttk.Frame(box, style="Card.TFrame")
        settings_frame.pack(pady=5)
        ttk.Label(settings_frame, text=i18n.t("set_duration"), style="Card.TLabel").pack(side="left", padx=(0, 5))
        e_timer_mins = ttk.Entry(settings_frame, textvariable=self.var_timer_mins, width=5, style="Dark.TEntry", justify="center")
        e_timer_mins.pack(side="left")
        self.var_timer_mins.trace_add("write", lambda *args: self._reset_timer())

        controls = ttk.Frame(box, style="Card.TFrame")
        controls.pack(pady=20)
        PillButton(controls, text=i18n.t("start"), command=self._start_timer).pack(side="left", padx=10)
        PillButton(controls, text=i18n.t("pause"), command=self._pause_timer).pack(side="left", padx=10)
        PillButton(controls, text=i18n.t("reset"), command=self._reset_timer).pack(side="left", padx=10)

        self._reset_timer()

        NavBar(self, on_home=self._build_home, on_add=self._add_popup,
               on_settings=self._open_settings, on_timer=self._build_timer).pack(pady=8)

    def _start_timer(self):
        if self.timer_running: return
        self.timer_running = True
        self._update_timer_display()

    def _pause_timer(self):
        self.timer_running = False

    def _reset_timer(self):
        self.timer_running = False
        self.timer_seconds = self._get_timer_duration_seconds()
        self._update_timer_display()

    def _update_timer_display(self):
        if self.timer_job: self.after_cancel(self.timer_job)
        if self.timer_running and self.timer_seconds > 0: self.timer_seconds -= 1
        mins, secs = divmod(self.timer_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        if self.timer_running and self.timer_seconds > 0:
            self.timer_job = self.after(1000, self._update_timer_display)
        elif self.timer_running and self.timer_seconds == 0:
            self.timer_running = False
            try:
                if winsound: winsound.Beep(1200, 500)
                else: self.bell()
            except Exception: self.bell()
            messagebox.showinfo(i18n.t("time_up"), i18n.t("take_a_break"))

    # ---------- tasks UI ----------
    def _build_tasks(self, parent):
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill="x", pady=(0, 8))

        self.e_task = ttk.Entry(row, width=40, style="Dark.TEntry")
        self.e_task.pack(side="left", fill="x", expand=True)
        self.e_task.bind("<Return>", self.add_task)

        self.e_due = ttk.Entry(row, width=10, style="Dark.TEntry")
        self.e_due.insert(0, "MM/DD")
        self.e_due.bind("<FocusIn>", lambda e: self._clear_placeholder(self.e_due, "MM/DD"))
        self.e_due.bind("<FocusOut>", lambda e: self._add_placeholder(self.e_due, "MM/DD"))
        self.e_due.bind("<KeyRelease>", self._due_entry_modified)
        self.e_due.pack(side="left", padx=(6,0))
        PillButton(row, text="📅", width=2, command=self._open_calendar).pack(side="left", padx=(2,6))

        self.var_pr = tk.StringVar(value=i18n.t("normal"))
        self.cmb_pr = ttk.Combobox(row, textvariable=self.var_pr, values=[i18n.t("normal"), i18n.t("medium"), i18n.t("high")],
                                    state="readonly", width=12, style="Dark.TCombobox")
        self.cmb_pr.pack(side="left", padx=6)

        PillButton(row, text=i18n.t("add_task"), command=self.add_task).pack(side="right")

        area = ttk.Frame(parent, style="Card.TFrame")
        area.pack(fill="both", expand=True)

        PALETTE = THEMES[i18n.theme]
        self.lb = tk.Listbox(area, height=10, bg=PALETTE["entry_bg"], fg=PALETTE["text"],
                             highlightthickness=0, selectbackground=PALETTE["accent"], relief=tk.FLAT,
                             activestyle="none", font=self.tasks_font)
        self.lb.pack(side="left", fill="both", expand=True, padx=(0, 6), pady=4)
        
        sb = ttk.Scrollbar(area, orient="vertical", command=self.lb.yview, style="App.Vertical.TScrollbar")
        sb.pack(side="right", fill="y")
        self.lb.config(yscrollcommand=sb.set)

        bar = ttk.Frame(parent, style="Card.TFrame")
        bar.pack(fill="x", pady=(6, 0))
        PillButton(bar, text=i18n.t("mark_done"), command=self.mark_done).pack(side="left", padx=(0, 6))
        PillButton(bar, text=i18n.t("delete"), command=self.delete_task).pack(side="left", padx=(0, 6))
        PillButton(bar, text=i18n.t("clear_completed"), command=self.clear_completed).pack(side="left")

    # ---------- helpers ----------
    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder: entry.delete(0, tk.END)

    def _add_placeholder(self, entry, placeholder):
        if not entry.get(): entry.insert(0, placeholder)
    
    def _open_calendar(self):
        def on_pick(date_obj):
            self._selected_due_date_obj = date_obj
            self.e_due.delete(0, tk.END)
            self.e_due.insert(0, date_obj.strftime("%m/%d"))
        open_calendar_popup(self, on_pick)

    def _due_entry_modified(self, event=None):
        self._selected_due_date_obj = None

    def _parse_due_datetime(self, md_str: str):
        md_str = (md_str or "").strip()
        if not md_str or md_str == "MM/DD": return None
        if not re.fullmatch(r"\d{1,2}/\d{1,2}", md_str): return None
        try:
            m, d = map(int, md_str.split("/"))
            year = date.today().year
            return datetime(year, m, d, 23, 59)
        except Exception:
            return None

    def _add_popup(self):
        messagebox.showinfo(i18n.t("add"), i18n.t("new_tip"))

    # ---------- actions ----------
    def add_task(self, event=None):
        t = self.e_task.get().strip()
        if not t:
            messagebox.showwarning("!", i18n.t("warn_enter_task"))
            return

        due_dt = None
        if self._selected_due_date_obj:
            y, m, d = self._selected_due_date_obj.year, self._selected_due_date_obj.month, self._selected_due_date_obj.day
            due_dt = datetime(y, m, d, 23, 59)
        else:
            due_dt = self._parse_due_datetime(self.e_due.get())
        
        pr = self.var_pr.get()
        s = f"[{pr}] {t} — Due: {due_dt.strftime('%m/%d')}" if due_dt else f"[{pr}] {t}"
        
        self.lb.insert(tk.END, s)
        idx = self.lb.size() - 1
        PALETTE = THEMES[i18n.theme]
        if pr == i18n.t("high"):
            self.lb.itemconfig(idx, fg=PALETTE["danger"])
            try:
                if winsound: winsound.Beep(1000, 200)
                else: self.bell()
            except Exception: pass
        elif pr == i18n.t("medium"):
            self.lb.itemconfig(idx, fg=PALETTE["accent3"])

        self.tasks_data.append({"text": t, "pr": pr, "due": due_dt, "done": False, "alerted": False})
        self.e_task.delete(0, tk.END)
        self.e_due.delete(0, tk.END); self.e_due.insert(0, "MM/DD")
        self.var_pr.set(i18n.t("normal"))
        self._selected_due_date_obj = None

    def delete_task(self):
        try:
            idx = self.lb.curselection()[0]
            self.lb.delete(idx)
            del self.tasks_data[idx]
        except Exception:
            messagebox.showwarning("!", i18n.t("warn_select_task"))
            
    def mark_done(self):
        try:
            i = self.lb.curselection()[0]
            s = self.lb.get(i)
            if not s.endswith(" (Done)"):
                self.lb.delete(i)
                self.lb.insert(i, s + " (Done)")
                PALETTE = THEMES[i18n.theme]
                self.lb.itemconfig(i, fg=PALETTE["muted"])
                self.tasks_data[i]["done"] = True
        except Exception:
            messagebox.showwarning("!", i18n.t("warn_select_task"))

    def clear_completed(self):
        for i in range(self.lb.size() - 1, -1, -1):
            if self.lb.get(i).endswith(" (Done)"):
                self.lb.delete(i)
                del self.tasks_data[i]

    # ---------- alerts ----------
    def _start_due_check(self):
        self._check_due_alerts()
        self.after(60_000, self._start_due_check)

    def _check_due_alerts(self):
        now = datetime.now()
        for task in self.tasks_data:
            if (not task["alerted"] and not task["done"] and task["due"] and
                task["pr"] == i18n.t("high") and now >= task["due"]):
                task["alerted"] = True
                try:
                    if winsound: winsound.Beep(1100, 400)
                    else: self.bell()
                except Exception: pass
                messagebox.showwarning("⏰ Due", f'High priority task due: "{task["text"]}"')

    # ---------- settings ----------
    def _open_settings(self):
        SettingsPopup(self, on_changed=self._rebuild_all)