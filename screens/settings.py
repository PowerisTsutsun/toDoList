import tkinter as tk
from tkinter import ttk, messagebox
from ui.i18n import i18n
from ui.theme import THEMES

class SettingsPopup(tk.Toplevel):
    def __init__(self, parent, on_changed=None):
        super().__init__(parent)
        self.title(i18n.t("settings"))
        self.resizable(False, False)
        self.on_changed = on_changed
        self.configure(bg="#0F1420") # Keep popup bg dark for consistency

        frm = ttk.Frame(self, padding=16)
        frm.pack(fill="both", expand=True)

        # --- Language ---
        ttk.Label(frm, text=i18n.t("language")).grid(row=0, column=0, sticky="w", pady=(0,8))
        self.var_lang = tk.StringVar(value=i18n.lang)
        lang_codes = list(i18n.languages.keys())
        lang_names = [i18n.languages[c] for c in lang_codes]
        self.combo_lang = ttk.Combobox(frm, state="readonly", values=lang_names, width=20)
        self.combo_lang.grid(row=0, column=1, padx=8, pady=(0,8))
        self.code_for_name = dict(zip(lang_names, lang_codes))
        self.combo_lang.set(i18n.languages[i18n.lang])

        # --- Theme ---
        ttk.Label(frm, text=i18n.t("theme")).grid(row=1, column=0, sticky="w", pady=(0,8))
        self.var_theme = tk.StringVar(value=i18n.theme)
        theme_names = list(THEMES.keys())
        self.combo_theme = ttk.Combobox(frm, state="readonly", values=theme_names, width=20)
        self.combo_theme.grid(row=1, column=1, padx=8, pady=(0,8))
        self.combo_theme.set(i18n.theme)

        def save():
            # Save Language
            lang_code = self.code_for_name[self.combo_lang.get()]
            i18n.set_lang(lang_code)

            # Save Theme
            theme_name = self.combo_theme.get()
            i18n.set_theme(theme_name)
            
            if callable(self.on_changed): self.on_changed()
            messagebox.showinfo(i18n.t("settings"), i18n.t("language_saved"))
            self.destroy()

        ttk.Button(frm, text="Save & Apply", command=save).grid(row=2, column=0, columnspan=2, pady=6, sticky="ew")