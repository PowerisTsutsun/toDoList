import tkinter as tk
from tkinter import ttk
from .theme import THEMES
from .i18n import i18n

def round_rect(c, x1,y1,x2,y2,r=18, **kw):
    pts=[x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r, x2,y2, x2-r,y2,
         x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1]
    return c.create_polygon(pts, smooth=True, **kw)

class Card(ttk.Frame):
    """Raised card with subtle shadow + inner frame for content."""
    def __init__(self, master, w=340, h=180, title=None, subtitle=None, tag=None):
        super().__init__(master, style="Card.TFrame")
        
        PALETTE = THEMES[i18n.theme]
        APP_BG = PALETTE["bg"]
        CARD_BG = PALETTE["card"]

        self.canvas = tk.Canvas(self, width=w, height=h, bg=APP_BG, highlightthickness=0)
        self.canvas.pack()
        # shadow + body
        round_rect(self.canvas, 10,16,w-6,h-2, r=22, fill="#0C1120" if i18n.theme == "Dark" else "#E5E7EB", outline="")
        round_rect(self.canvas, 4,6,w-12,h-10, r=22, fill=CARD_BG, outline=PALETTE["border"])
        self.inner = ttk.Frame(self, style="Card.TFrame")
        self.inner.place(in_=self.canvas, x=18, y=16, relwidth=0.92, height=h-34)

        if title:
            top = ttk.Frame(self.inner, style="Card.TFrame")
            top.pack(fill="x")
            if tag:
                chip = tk.Label(top, text=tag, bg=PALETTE["card_hi"], fg=PALETTE["accent"],
                                padx=10, pady=4, font=("Segoe UI", 9, "bold"))
                chip.pack(side="left", padx=(0,8))

            # Vertical text frame for better alignment
            text_frame = ttk.Frame(top, style="Card.TFrame")
            text_frame.pack(side="left", fill="x", expand=True, padx=4)

            ttk.Label(text_frame, text=title, style="Card.TLabel",
                      font=("Segoe UI", 16, "bold")).pack(anchor="w")
            if subtitle:
                ttk.Label(text_frame, text=subtitle, style="Card.TLabel",
                          foreground=PALETTE["muted"]).pack(anchor="w")

class GlowTile(tk.Frame):
    """Clickable tile with cyan border glow (like the screenshot)."""
    def __init__(self, master, title, value, accent="accent", command=None, w=150, h=90):
        PALETTE = THEMES[i18n.theme]
        APP_BG = PALETTE["bg"]
        CARD_BG = PALETTE["card"]
        
        super().__init__(master, bg=APP_BG)
        self.command = command
        c = tk.Canvas(self, width=w, height=h, bg=APP_BG, highlightthickness=0)
        c.pack()
        border = PALETTE[accent]
        round_rect(c, 2, 6, w-2, h-2, r=18, fill=CARD_BG, outline=border)
        self.lbl1 = tk.Label(self, text=title, bg=CARD_BG, fg=PALETTE["muted"], font=("Segoe UI",9))
        self.lbl2 = tk.Label(self, text=value, bg=CARD_BG, fg=PALETTE["text"],  font=("Segoe UI",14,"bold"))
        self.lbl1.place(x=16,y=16); self.lbl2.place(x=16,y=40)

        def enter(_):
            c.itemconfig(1, outline=PALETTE["accent2"])
        def leave(_):
            c.itemconfig(1, outline=border)
        def click(_):
            if self.command: self.command()

        c.bind("<Enter>", enter); c.bind("<Leave>", leave); c.bind("<Button-1>", click)
        self.lbl1.bind("<Button-1>", click); self.lbl2.bind("<Button-1>", click)

class NavBar(tk.Frame):
    """Bottom bar with icons: Home, Timer, Add, Settings."""
    def __init__(self, master, on_home, on_add, on_settings, on_timer):
        PALETTE = THEMES[i18n.theme]
        APP_BG = PALETTE["bg"]
        CARD_BG = PALETTE["card"]
        
        super().__init__(master, bg=APP_BG)
        c = tk.Canvas(self, width=700, height=76, bg=APP_BG, highlightthickness=0)
        c.pack()
        round_rect(c, 12, 10, 688, 66, r=22, fill=CARD_BG, outline=PALETTE["border"])
        # buttons
        def mk(x, text, cb):
            b = tk.Label(c, text=text, bg=CARD_BG, fg=PALETTE["muted"], font=("Segoe UI",10,"bold"))
            b.place(x=x, y=26)
            b.bind("<Button-1>", lambda *_: cb())
            return b
        mk(80, "Home", on_home)
        mk(230, "Timer", on_timer)
        mk(380, "+", on_add)
        mk(530, "Settings", on_settings)

class PillButton(ttk.Button):
    def __init__(self, master, text, **kw):
        super().__init__(master, text=text, style="Chip.TButton", **kw)