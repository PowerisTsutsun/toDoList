import json, os

# --- Config Management ---
_CFG = "config.json"
config = {"lang": "en", "theme": "Dark", "username": "Valance"}

def load_config():
    if os.path.exists(_CFG):
        try:
            with open(_CFG, "r", encoding="utf-8") as f: config.update(json.load(f))
        except Exception: pass

def save_config():
    try:
        with open(_CFG, "w", encoding="utf-8") as f: json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception: pass

# --- Translations ---
_LANGS = {
    "en": {
        "app_title": "To-Do (Dark)", "home": "Home", "name": "Name", "settings": "Settings",
        "settings_saved": "Settings saved and applied!", "theme": "Theme", "dark": "Dark", "light": "Light",
        "timer": "Timer", "pomodoro": "Pomodoro Timer", "start": "Start", "pause": "Pause",
        "reset": "Reset", "set_duration": "Duration (min):", "time_up": "Time's up!",
        "take_a_break": "Time for a short break.", "hello_name": "Hello, {name} 👋",
        "welcome": "Welcome back", "today": "Today", "tasks": "Tasks", "completed": "Completed",
        "clear": "Clear", "list": "List", "add_task": "Add Task", "select_all": "Select All",
        "due_date": "Due Date", "priority": "Priority", "high": "High", "medium": "Medium",
        "normal": "Normal", "mark_done": "✓ Complete", "delete": "🗑 Delete",
        "warn_enter_task": "Please enter a task.", "warn_select_task": "Select a task first.",
        "new_tip": "Use the input to add a task.", "notifications": "Notifications",
        "alerts": "Alerts", "high_priority": "High Priority", "language": "Language",
    },
    "es": {
        "app_title": "To-Do (Oscuro)", "home": "Inicio", "name": "Nombre", "settings": "Ajustes",
        "settings_saved": "Ajustes guardados y aplicados.", "theme": "Tema", "dark": "Oscuro", "light": "Claro",
        "timer": "Reloj", "pomodoro": "Temporizador Pomodoro", "start": "Iniciar", "pause": "Pausa",
        "reset": "Reiniciar", "set_duration": "Duración (min):", "time_up": "¡Se acabó el tiempo!",
        "take_a_break": "Es hora de un breve descanso.", "hello_name": "Hola, {name} 👋",
        "welcome": "Bienvenido", "today": "Hoy", "tasks": "Tareas", "completed": "Completadas",
        "clear": "Limpiar", "list": "Lista", "add_task": "Añadir", "select_all": "Seleccionar todo",
        "due_date": "Fecha", "priority": "Prioridad", "high": "Alta", "medium": "Media",
        "normal": "Normal", "mark_done": "✓ Completar", "delete": "🗑 Eliminar",
        "warn_enter_task": "Escribe una tarea.", "warn_select_task": "Selecciona una tarea.",
        "new_tip": "Usa el cuadro para añadir una tarea.", "notifications": "Notificaciones",
        "alerts": "Alertas", "high_priority": "Prioridad Alta", "language": "Idioma",
    },
}

class I18N:
    def __init__(self):
        load_config()
        self.lang = config["lang"]
        self.theme = config["theme"]
        self.username = config["username"]
    @property
    def languages(self): return {"en": "English", "es": "Español"}
    def t(self, key, **fmt):
        text = _LANGS.get(self.lang, _LANGS["en"]).get(key, key)
        return text.format(**fmt) if fmt else text
    def set_lang(self, code):
        if code in _LANGS: self.lang = code; config["lang"] = code; save_config()
    def set_theme(self, theme_name):
        self.theme = theme_name; config["theme"] = theme_name; save_config()
    def set_username(self, name):
        self.username = name; config["username"] = name; save_config()

i18n = I18N()