import json, os

# --- Config Management ---
_CFG = "config.json"
config = {
    "lang": "en",
    "theme": "Dark"
}

def load_config():
    if os.path.exists(_CFG):
        try:
            with open(_CFG, "r", encoding="utf-8") as f:
                loaded_config = json.load(f)
                config.update(loaded_config)
        except Exception:
            pass # Use default config

def save_config():
    try:
        with open(_CFG, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# --- Translations ---
_LANGS = {
    "en": {
        "app_title": "To-Do (Dark)",
        "home": "Home",
        "add": "Add",
        "settings": "Settings",
        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",
        "theme_saved": "Theme saved. Restart not required.",
        "timer": "Timer",
        "pomodoro": "Pomodoro Timer",
        "start": "Start",
        "pause": "Pause",
        "reset": "Reset",
        "set_duration": "Duration (min):",
        "time_up": "Time's up!",
        "take_a_break": "Time for a short break.",
        "hello_name": "Hello, {name} 👋",
        "welcome": "Welcome back",
        "today": "Today",
        "tasks": "Tasks",
        "completed": "Completed",
        "list": "List",
        "add_task": "Add Task",
        "due_date": "Due Date",
        "priority": "Priority",
        "high": "High",
        "medium": "Medium",
        "normal": "Normal",
        "mark_done": "✓ Complete",
        "delete": "🗑 Delete",
        "clear_completed": "Clear Completed",
        "warn_enter_task": "Please enter a task.",
        "warn_select_task": "Select a task first.",
        "new_tip": "Use the input to add a task.",
        "notifications": "Notifications",
        "alerts": "Alerts",
        "high_priority": "High Priority",
        "language": "Language",
        "language_saved": "Language saved. Restart not required.",
    },
    "es": {
        "app_title": "To-Do (Oscuro)",
        "home": "Inicio",
        "add": "Añadir",
        "settings": "Ajustes",
        "theme": "Tema",
        "dark": "Oscuro",
        "light": "Claro",
        "theme_saved": "Tema guardado. No hace falta reiniciar.",
        "timer": "Reloj",
        "pomodoro": "Temporizador Pomodoro",
        "start": "Iniciar",
        "pause": "Pausa",
        "reset": "Reiniciar",
        "set_duration": "Duración (min):",
        "time_up": "¡Se acabó el tiempo!",
        "take_a_break": "Es hora de un breve descanso.",
        "hello_name": "Hola, {name} 👋",
        "welcome": "Bienvenido",
        "today": "Hoy",
        "tasks": "Tareas",
        "completed": "Completadas",
        "list": "Lista",
        "add_task": "Añadir",
        "due_date": "Fecha",
        "priority": "Prioridad",
        "high": "Alta",
        "medium": "Media",
        "normal": "Normal",
        "mark_done": "✓ Completar",
        "delete": "🗑 Eliminar",
        "clear_completed": "Limpiar Completadas",
        "warn_enter_task": "Escribe una tarea.",
        "warn_select_task": "Selecciona una tarea.",
        "new_tip": "Usa el cuadro para añadir una tarea.",
        "notifications": "Notificaciones",
        "alerts": "Alertas",
        "high_priority": "Prioridad Alta",
        "language": "Idioma",
        "language_saved": "Idioma guardado. No hace falta reiniciar.",
    },
}

class I18N:
    def __init__(self):
        load_config() # Load config on init
        self.lang = config["lang"]
        self.theme = config["theme"]

    @property
    def languages(self):
        return {"en": "English", "es": "Español"}

    def t(self, key, **fmt):
        text = _LANGS.get(self.lang, _LANGS["en"]).get(key, key)
        return text.format(**fmt) if fmt else text

    def set_lang(self, code):
        if code in _LANGS:
            self.lang = code
            config["lang"] = code
            save_config()
    
    def set_theme(self, theme_name):
        self.theme = theme_name
        config["theme"] = theme_name
        save_config()

# singleton
i18n = I18N()