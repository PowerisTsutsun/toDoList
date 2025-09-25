import sys, re, tkinter as tk
from tkinter import ttk, messagebox, font, Toplevel
from datetime import date, datetime
from ui.theme import apply_theme, THEMES
from ui.widgets import Card, GlowTile, NavBar, PillButton
from ui.i18n import i18n
from ui.calendar import open_calendar_popup

try:
    import winsound
except Exception:
    winsound = None

class TodoScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="App.TFrame", padding=(0, 16, 0, 0))
        self.master = master
        self.pack(fill="both", expand=True)
        
        self.tasks_font = font.Font(family="Segoe UI", size=11, weight="bold")

        if not hasattr(master, 'tasks_data'):
             master.tasks_data = [] 
        self.tasks_data = master.tasks_data

        self._selected_due_date_obj = None
        self.var_timer_mins = tk.StringVar(value="25")
        self.timer_seconds = 25 * 60
        self.timer_running = False
        self.timer_job = None
        self.settings_frame = None

        self._build_home()
        if not hasattr(master, '_alert_job_started'):
            self._start_due_check()
            master._alert_job_started = True

    def _clear(self):
        if self.timer_job: self.after_cancel(self.timer_job)
        for w in self.winfo_children(): w.destroy()

    def _rebuild_all(self):
        self.destroy()
        apply_theme(self.master, i18n.theme)
        TodoScreen(self.master)

    def _get_tasks_due_today_count(self):
        return sum(1 for task in self.tasks_data if task.get("due") and task["due"].date() == date.today() and not task.get("done"))

    def _build_home(self):
        self._clear()
        
        self.nav_bar = NavBar(self, on_home=self._build_home, on_timer=self._build_timer,
               on_add=self._add_popup, on_settings=self._toggle_settings_panel)
        self.nav_bar.pack(side="bottom", fill="x", pady=(10, 16))

        head = Card(self, title=i18n.t("hello_name", name=i18n.username),
                    subtitle=i18n.t("welcome"), tag="🏠")
        head.pack(pady=(0, 12))

        action_tiles_frame = ttk.Frame(self, style="App.TFrame")
        action_tiles_frame.pack(pady=6)
        GlowTile(action_tiles_frame, "Due Today", f"{self._get_tasks_due_today_count()}", "accent2").pack(side="left", padx=8)
        GlowTile(action_tiles_frame, i18n.t("today"), date.today().strftime("%d %b"), "accent").pack(side="left", padx=8)

        list_card = Card(self, title=i18n.t("tasks"), tag=i18n.t("list"))
        list_card.pack(pady=10, fill="both", expand=True)
        self._build_tasks(list_card.inner)

    def _build_timer(self):
        self._clear()
        self.timer_running = False

        self.nav_bar = NavBar(self, on_home=self._build_home, on_timer=self._build_timer,
               on_add=self._add_popup, on_settings=self._toggle_settings_panel)
        self.nav_bar.pack(side="bottom", fill="x", pady=(10, 16))

        top = Card(self, title=i18n.t("pomodoro"), tag="⏱️")
        top.pack(pady=10, fill="both", expand=True)
        box = top.inner
        
        self.timer_label = ttk.Label(box, text="25:00", font=("Segoe UI", 88, "bold"), style="Card.TLabel")
        self.timer_label.pack(pady=10, expand=True)

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

    def _build_tasks(self, parent):
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill="x", pady=(0, 8))

        button_stack = ttk.Frame(row, style="Card.TFrame")
        button_stack.pack(side="right", padx=(6,0))
        PillButton(button_stack, text=i18n.t("clear"), command=self.clear_completed).pack(fill="x")
        PillButton(button_stack, text=i18n.t("select_all"), command=self._select_all_tasks).pack(fill="x", pady=(4,0))
        PillButton(button_stack, text=i18n.t("add_task"), command=self.add_task, style="Accent.Chip.TButton").pack(fill="x", pady=(4,0))
        
        input_frame = ttk.Frame(row, style="Card.TFrame")
        input_frame.pack(side="left", fill="x", expand=True)
        self.e_task = ttk.Entry(input_frame, style="Dark.TEntry")
        self.e_task.pack(side="left", fill="x", expand=True)
        self.e_task.bind("<Return>", self.add_task)
        self.e_due = ttk.Entry(input_frame, width=10, style="Dark.TEntry")
        self.e_due.insert(0, "MM/DD")
        self.e_due.bind("<FocusIn>", lambda e: self._clear_placeholder(self.e_due, "MM/DD"))
        self.e_due.bind("<FocusOut>", lambda e: self._add_placeholder(self.e_due, "MM/DD"))
        self.e_due.pack(side="left", padx=(6,0))
        PillButton(input_frame, text="📅", width=2, command=self._open_calendar).pack(side="left", padx=(2,6))
        self.var_pr = tk.StringVar(value=i18n.t("normal"))
        self.cmb_pr = ttk.Combobox(input_frame, textvariable=self.var_pr, values=[i18n.t("normal"), i18n.t("medium"), i18n.t("high")],
                                    state="readonly", width=12, style="Dark.TCombobox")
        self.cmb_pr.pack(side="left")

        area = ttk.Frame(parent, style="Card.TFrame")
        area.pack(fill="both", expand=True)
        PALETTE = THEMES[i18n.theme]
        self.lb = tk.Listbox(area, height=10, bg=PALETTE["entry_bg"], fg=PALETTE["text"],
                             highlightthickness=0, selectbackground=PALETTE["accent"], relief=tk.FLAT,
                             activestyle="none", font=self.tasks_font, selectmode="extended")
        self.lb.pack(side="left", fill="both", expand=True, padx=(0, 6), pady=4)
        sb = ttk.Scrollbar(area, orient="vertical", command=self.lb.yview, style="App.Vertical.TScrollbar")
        sb.pack(side="right", fill="y")
        self.lb.config(yscrollcommand=sb.set)

        self.task_map = {}
        for i, task in enumerate(self.tasks_data):
            s = f"[{task['pr']}] {task['text']} — Due: {task['due'].strftime('%m/%d')}" if task['due'] else f"[{task['pr']}] {task['text']}"
            if task.get("done"): s += " (Done)"
            self.lb.insert(tk.END, s)
            listbox_index = self.lb.size() - 1
            self.task_map[listbox_index] = i
            if task.get("done"): self.lb.itemconfig(listbox_index, fg=PALETTE["muted"])
            elif task['pr'] == i18n.t("high"): self.lb.itemconfig(listbox_index, fg=PALETTE["danger"])
            elif task['pr'] == i18n.t("medium"): self.lb.itemconfig(listbox_index, fg=PALETTE["accent3"])

        bar = ttk.Frame(parent, style="Card.TFrame")
        bar.pack(fill="x", pady=(6, 0))
        PillButton(bar, text=i18n.t("mark_done"), command=self.mark_done).pack(side="left", padx=(0, 6))
        PillButton(bar, text=i18n.t("delete"), command=self.delete_task).pack(side="left", padx=(0, 6))

    def _toggle_settings_panel(self):
        if self.settings_frame and self.settings_frame.winfo_exists():
            self.settings_frame.destroy(); self.settings_frame = None; return
        self.settings_frame = Card(self, title=i18n.t("settings"), tag="⚙️")
        self.settings_frame.pack(side="bottom", before=self.nav_bar, pady=10)
        frm = self.settings_frame.inner
        name_frame = ttk.Frame(frm, style="Card.TFrame"); name_frame.pack(fill="x", expand=True, pady=4)
        ttk.Label(name_frame, text=i18n.t("name"), style="Card.TLabel").pack(side="left")
        name_var = tk.StringVar(value=i18n.username)
        entry_name = ttk.Entry(name_frame, textvariable=name_var, width=22, style="Dark.TEntry"); entry_name.pack(side="right")
        lang_frame = ttk.Frame(frm, style="Card.TFrame"); lang_frame.pack(fill="x", expand=True, pady=4)
        ttk.Label(lang_frame, text=i18n.t("language"), style="Card.TLabel").pack(side="left")
        lang_codes=list(i18n.languages.keys()); lang_names=[i18n.languages[c] for c in lang_codes]
        combo_lang = ttk.Combobox(lang_frame, state="readonly", values=lang_names, width=20, style="Dark.TCombobox"); combo_lang.pack(side="right")
        code_for_name = dict(zip(lang_names, lang_codes)); combo_lang.set(i18n.languages[i18n.lang])
        theme_frame = ttk.Frame(frm, style="Card.TFrame"); theme_frame.pack(fill="x", expand=True, pady=4)
        ttk.Label(theme_frame, text=i18n.t("theme"), style="Card.TLabel").pack(side="left")
        theme_names = list(THEMES.keys())
        combo_theme = ttk.Combobox(theme_frame, state="readonly", values=theme_names, width=20, style="Dark.TCombobox"); combo_theme.pack(side="right")
        combo_theme.set(i18n.theme)
        def save():
            i18n.set_username(name_var.get()); i18n.set_lang(code_for_name[combo_lang.get()]); i18n.set_theme(combo_theme.get())
            messagebox.showinfo(i18n.t("settings"), i18n.t("settings_saved")); self._rebuild_all()
        PillButton(frm, text="Save & Apply", command=save).pack(fill="x", expand=True, pady=10)

    # --- Action Methods ---
    def _select_all_tasks(self): self.lb.selection_set(0, 'end')
    def add_task(self, event=None):
        t = self.e_task.get().strip()
        if not t: return messagebox.showwarning("!", i18n.t("warn_enter_task"))
        due_dt = datetime(self._selected_due_date_obj.year, self._selected_due_date_obj.month, self._selected_due_date_obj.day, 23, 59) if self._selected_due_date_obj else self._parse_due_datetime(self.e_due.get())
        pr = self.var_pr.get()
        self.tasks_data.append({"text": t, "pr": pr, "due": due_dt, "done": False, "alerted": False})
        if pr == i18n.t("high"):
            try:
                if winsound: winsound.Beep(1000, 200)
                else: self.bell()
            except Exception: pass
        self._build_home()
    def delete_task(self):
        try:
            selected_indices = self.lb.curselection()
            data_indices_to_delete = sorted([self.task_map[i] for i in selected_indices], reverse=True)
            for data_idx in data_indices_to_delete: del self.tasks_data[data_idx]
            self._build_home()
        except Exception: messagebox.showwarning("!", i18n.t("warn_select_task"))
    def mark_done(self):
        try:
            selected_indices = self.lb.curselection()
            for listbox_idx in selected_indices:
                data_idx = self.task_map[listbox_idx]
                task = self.tasks_data[data_idx]
                task["done"] = not task.get("done", False)
            self._build_home()
        except Exception: messagebox.showwarning("!", i18n.t("warn_select_task"))
    def clear_completed(self):
        selected_indices = self.lb.curselection()
        if not selected_indices:
            messagebox.showwarning("!", i18n.t("warn_select_task"))
            return
        data_indices_to_delete = sorted([self.task_map[i] for i in selected_indices], reverse=True)
        for idx in data_indices_to_delete:
            del self.tasks_data[idx]
        self._build_home()


    # --- Other methods ---
    def _get_timer_duration_seconds(self):
        try: val = self.var_timer_mins.get(); return max(1, int(val))*60 if val else 25*60
        except (ValueError, tk.TclError): return 25 * 60
    def _start_timer(self):
        if self.timer_running: return
        self.timer_running = True; self._update_timer_display()
    def _pause_timer(self): self.timer_running = False
    def _reset_timer(self):
        self.timer_running = False; self.timer_seconds = self._get_timer_duration_seconds(); self._update_timer_display()
    def _update_timer_display(self):
        if self.timer_job: self.after_cancel(self.timer_job)
        if self.timer_running and self.timer_seconds > 0: self.timer_seconds -= 1
        mins, secs = divmod(self.timer_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        if self.timer_running and self.timer_seconds > 0: self.timer_job = self.after(1000, self._update_timer_display)
        elif self.timer_running and self.timer_seconds == 0:
            self.timer_running = False
            try:
                if winsound: winsound.Beep(1200, 500)
                else: self.bell()
            except Exception: self.bell()
            messagebox.showinfo(i18n.t("time_up"), i18n.t("take_a_break"))
    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder: entry.delete(0, tk.END)
    def _add_placeholder(self, entry, placeholder):
        if not entry.get(): entry.insert(0, placeholder)
    def _open_calendar(self):
        def on_pick(d): self._selected_due_date_obj=d; self.e_due.delete(0,tk.END); self.e_due.insert(0,d.strftime("%m/%d"))
        open_calendar_popup(self, on_pick)
    def _due_entry_modified(self, e=None): self._selected_due_date_obj = None
    def _parse_due_datetime(self, md_str: str):
        md_str = (md_str or "").strip()
        if not md_str or md_str == "MM/DD" or not re.fullmatch(r"\d{1,2}/\d{1,2}", md_str): return None
        try: m, d = map(int, md_str.split("/")); return datetime(date.today().year, m, d, 23, 59)
        except Exception: return None
    def _add_popup(self): messagebox.showinfo(i18n.t("new_tip"), i18n.t("new_tip"))
    def _start_due_check(self): 
        self._check_due_alerts()
        self.master.after(60_000, self._start_due_check)
    def _check_due_alerts(self):
        now = datetime.now()
        for task in self.tasks_data:
            if not task.get("alerted") and not task.get("done") and task.get("due") and task.get("pr") == i18n.t("high") and now >= task["due"]:
                task["alerted"] = True
                try:
                    if winsound: winsound.Beep(1100, 400)
                    else: self.bell()
                except Exception: pass
                messagebox.showwarning("⏰ Due", f'High priority task due: "{task["text"]}"')