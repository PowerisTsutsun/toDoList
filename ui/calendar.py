from tkinter import ttk, Toplevel
import calendar
from datetime import date, timedelta
from .theme import THEMES
from .i18n import i18n

class MonthCalendar(ttk.Frame):
    """Pure-Tk month calendar with prev/next + selectable dates."""
    def __init__(self, master, on_select, start_date=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_select = on_select
        self.today = date.today()
        self.current = start_date or self.today.replace(day=1)
        self.selected = None
        self._build()

    def _build(self):
        for w in self.winfo_children(): w.destroy()
        
        # Get the current theme's palette
        PALETTE = THEMES[i18n.theme]

        header = ttk.Frame(self); header.pack(fill="x", pady=(0,6))
        ttk.Button(header, text="◀", width=3, command=self.prev_month).pack(side="left")
        ttk.Label(header, text=self.current.strftime("%B %Y"),
                  font=("Segoe UI", 11, "bold")).pack(side="left", expand=True)
        ttk.Button(header, text="▶", width=3, command=self.next_month).pack(side="right")

        grid = ttk.Frame(self); grid.pack()
        for i, wd in enumerate(["SUN","MON","TUE","WED","THU","FRI","SAT"]):
            ttk.Label(grid, text=wd, foreground=PALETTE["muted"]).grid(row=0, column=i, padx=4, pady=2)

        cal = calendar.Calendar(firstweekday=6)  # Sunday
        weeks = cal.monthdatescalendar(self.current.year, self.current.month)
        self._day_buttons = []
        for r, week in enumerate(weeks, start=1):
            for c, d in enumerate(week):
                btn = ttk.Button(grid, text=str(d.day), width=3,
                                 command=lambda dd=d: self.select(dd))
                btn.grid(row=r, column=c, padx=6, pady=4)
                if d.month != self.current.month:
                    btn.state(["disabled"])
                    btn.configure(style="Muted.TButton")
                else:
                    if d == self.today:
                        btn.configure(style="Today.TButton")
                self._day_buttons.append((d, btn))
        self._refresh_selection()

    def _refresh_selection(self):
        for d, b in self._day_buttons:
            if "disabled" in b.state(): continue
            if self.selected == d:
                b.configure(style="Selected.TButton")
            elif d == self.today:
                b.configure(style="Today.TButton")
            else:
                b.configure(style="TButton")

    def select(self, d):
        self.selected = d
        self._refresh_selection()
        if callable(self.on_select):
            self.on_select(d)

    def prev_month(self):
        self.current = (self.current - timedelta(days=1)).replace(day=1)
        self._build()

    def next_month(self):
        y = self.current.year + (1 if self.current.month == 12 else 0)
        m = 1 if self.current.month == 12 else self.current.month + 1
        self.current = self.current.replace(year=y, month=m, day=1)
        self._build()

def open_calendar_popup(parent, on_date_selected):
    """
    Opens a small popup with MonthCalendar.
    on_date_selected: callback(datetime.date) receiving the picked date object.
    """
    top = Toplevel(parent)
    top.title("Pick a date")
    top.resizable(False, False)
    
    # Set background based on theme for the popup window itself
    PALETTE = THEMES[i18n.theme]
    top.configure(bg=PALETTE["card"])

    def _picked(d):
        on_date_selected(d)
        top.destroy()
    
    cal = MonthCalendar(top, on_select=_picked, style="Card.TFrame")
    cal.pack(padx=10, pady=10)