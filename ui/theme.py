from tkinter import ttk

# --- COLOR PALETTES ---
THEMES = {
    "Dark": {
        "bg":        "#0F1420", "card": "#151C2B", "card_hi": "#1B2335", "border": "#24314A",
        "accent":    "#4DD0E1", "accent2": "#FF7BD2", "accent3": "#FFD166",
        "muted":     "#97A0B3", "text": "#E9EEF8", "danger": "#FF6B6B", "success": "#7CF29C",
        "entry_bg":  "#0E1320", "entry_fg": "#E9EEF8", "entry_focus": "#0C1829",
        "scroll_thumb": "#24314A", "scroll_hover": "#4DD0E1",
    },
    "Light": {
        "bg":        "#F3F4F6", "card": "#FFFFFF", "card_hi": "#F9FAFB", "border": "#E5E7EB",
        "accent":    "#06B6D4", "accent2": "#EC4899", "accent3": "#F59E0B",
        "muted":     "#6B7280", "text": "#1F2937", "danger": "#EF4444", "success": "#10B981",
        "entry_bg":  "#FFFFFF", "entry_fg": "#1F2937", "entry_focus": "#FFFFFF",
        "scroll_thumb": "#D1D5DB", "scroll_hover": "#06B6D4",
    },
    "Oceanic": {
        "bg":        "#0B1D2E", "card": "#122C44", "card_hi": "#1A3A5A", "border": "#2A557F",
        "accent":    "#33FFB5", "accent2": "#FF8A80", "accent3": "#FFD180",
        "muted":     "#A0B3C4", "text": "#E0F7FA", "danger": "#FF5252", "success": "#7CF29C",
        "entry_bg":  "#0A1826", "entry_fg": "#E0F7FA", "entry_focus": "#122C44",
        "scroll_thumb": "#2A557F", "scroll_hover": "#33FFB5",
    },
    "Forest": {
        "bg":        "#1A201A", "card": "#2B342B", "card_hi": "#3A453A", "border": "#4F5D4F",
        "accent":    "#FFAB00", "accent2": "#F50057", "accent3": "#76FF03",
        "muted":     "#B0A9A0", "text": "#F1F0ED", "danger": "#FF6B6B", "success": "#76FF03",
        "entry_bg":  "#141A14", "entry_fg": "#F1F0ED", "entry_focus": "#2B342B",
        "scroll_thumb": "#4F5D4F", "scroll_hover": "#FFAB00",
    }
}

# --- THEME APPLICATION ---
def apply_theme(root, theme_name="Dark"):
    PALETTE = THEMES.get(theme_name, THEMES["Dark"])
    APP_BG  = PALETTE["bg"]
    CARD_BG = PALETTE["card"]

    root.configure(bg=APP_BG)
    s = ttk.Style(root)
    try:
        s.theme_use("clam")
    except Exception:
        pass

    s.layout('App.Vertical.TScrollbar', 
        [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', 
            {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
    s.configure('App.Vertical.TScrollbar', troughcolor=PALETTE["entry_bg"], background=PALETTE["entry_bg"], borderwidth=0, arrowsize=0)
    s.map('App.Vertical.TScrollbar', background=[('active', PALETTE["scroll_hover"])],)
    s.configure('Vertical.Scrollbar.thumb', background=PALETTE["scroll_thumb"], relief='flat', borderwidth=0)

    s.configure(".", background=APP_BG, foreground=PALETTE["text"], borderwidth=0, focuscolor=APP_BG)
    s.configure("App.TFrame", background=APP_BG)
    s.configure("Card.TFrame", background=CARD_BG)
    s.configure("App.TLabel", background=APP_BG, foreground=PALETTE["text"])
    s.configure("Card.TLabel", background=CARD_BG, foreground=PALETTE["text"])
    s.configure("App.TSeparator", background=PALETTE["border"])

    s.configure("Dark.TEntry", fieldbackground=PALETTE["entry_bg"], foreground=PALETTE["entry_fg"], borderwidth=1, padding=6)
    s.map("Dark.TEntry", bordercolor=[('focus', PALETTE["accent"])], fieldbackground=[("focus", PALETTE["entry_focus"])])
    
    root.option_add('*TCombobox*Listbox*Background', PALETTE["entry_bg"])
    root.option_add('*TCombobox*Listbox*Foreground', PALETTE["entry_fg"])
    root.option_add('*TCombobox*Listbox*selectBackground', PALETTE["accent"])
    root.option_add('*TCombobox*Listbox*selectForeground', PALETTE["text"])
    
    s.configure("Dark.TCombobox", fieldbackground=PALETTE["entry_bg"], foreground=PALETTE["entry_fg"], arrowcolor=PALETTE["text"], borderwidth=1)
    s.map("TCombobox", bordercolor=[('focus', PALETTE["accent"])], fieldbackground=[("readonly", PALETTE["entry_bg"])])

    s.configure("Chip.TButton", relief="flat", padding=(12,8), background=PALETTE["card"], foreground=PALETTE["text"])
    s.map("Chip.TButton", background=[("active", PALETTE["card_hi"])], relief=[("pressed", "sunken")])

    # New style for highlighted button
    s.configure("Accent.Chip.TButton", background=PALETTE["accent"], foreground=PALETTE["text"])
    s.map("Accent.Chip.TButton", background=[("active", PALETTE["accent2"])])

    root.listbox_bg = PALETTE["entry_bg"]

    s.configure("Muted.TButton", foreground=PALETTE["muted"])
    s.configure("Today.TButton")
    s.map("Today.TButton", background=[("!disabled", PALETTE["card_hi"])])
    s.configure("Selected.TButton")
    s.map("Selected.TButton", background=[("!disabled", PALETTE["accent"])], foreground=[("!disabled", PALETTE["text"])])