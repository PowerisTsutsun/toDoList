# To-Do-App

A simple, themed Tkinter to-do app with i18n, priority + due dates, and a built-in Pomodoro timer.

## Features
- ✅ Add tasks with optional **due date** (MM/DD) and **priority** (Normal/Medium/High)
- ✅ **Mark Done**, **Delete**, and **Clear** (behavior configurable: completed / selected / all)
- ✅ **Select All** convenience button
- ✅ **Pomodoro Timer** with Start/Pause/Reset and custom duration
- ✅ **High-priority alerts** when due
- 🎨 **Themes**, 🌐 **English/Spanish** i18n, and personalized greeting

## Getting Started

### Requirements
- Python 3.9+ (recommended)
- Windows/macOS/Linux

### Install
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt  # if present
# If no requirements.txt, Tkinter ships with most Python builds; you may just run it.
```
# Run
` python main.py `

# Usage

- Add Task: type in the task, optional MM/DD in due field, pick priority, hit Enter or click Add Task.
- Select All: selects every task in the list (useful before Mark Done or Delete).
- Mark Done: toggles done status on selected tasks.
- Delete: deletes selected tasks.
- Clear:
  - If you keep the default behavior from code, it clears completed tasks.
  - You can switch to “clear selected” or “clear all” (see Customization below).

# Pomodoro
- Set minutes in the input, then Start, Pause, Reset.
- The app beeps (or rings bell) on completion and shows a break message.

# Configuration (config.json)

- The app reads and writes a small config file to remember your preferences
```
{
  "lang": "en",        // "en" or "es"
  "theme": "Dark",     // must match a key in THEMES
  "username": "User's name"
}
```

# Project Structure (key parts)

- ui/todos.py — main screen logic (listbox, buttons, timer, alerts)

- ui/i18n.py — language strings + config load/save

- ui/theme.py — theme definitions and apply_theme

- ui/widgets.py — custom widgets (Card, GlowTile, etc.)

```
Feel free to fork the repo, improve the solver, and submit pull requests! 💡
```
