from tkinter import Tk
from ui.theme import apply_theme
from ui.i18n import i18n
from screens.todos import TodoScreen

def main():
    root = Tk()
    root.title(i18n.t("app_title"))
    root.geometry("740x680")
    
    apply_theme(root, i18n.theme) # Apply saved theme on startup
    
    TodoScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()