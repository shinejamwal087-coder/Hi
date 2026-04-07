# Simple Daily Utility App (Phase 1 MVP)

A lightweight Android-first Kivy app with:
- Bottom tab navigation (Home, Notes, Reminders, Assistant placeholder)
- Notes system (add/list/delete)
- Basic reminder system (add/list/delete with category + repeat)
- Local SQLite storage

## Project Structure

```text
.
├── main.py
├── buildozer.spec
├── data/
│   └── storage.py
├── logic/
│   ├── notes_manager.py
│   └── reminder_manager.py
└── ui/
    └── screens.py
```

## Requirements

- Python 3.9+
- Kivy

Install:

```bash
pip install kivy
```

## Run (Desktop test)

```bash
python main.py
```

## Run in Pydroid 3 (Android)

1. Install **Pydroid 3** from Play Store.
2. Open Pydroid terminal and install Kivy:
   ```bash
   pip install kivy
   ```
3. Copy this project folder to your phone storage.
4. Open `main.py` in Pydroid and press **Run**.

## Run in Termux (Android)

> Note: Kivy support in Termux varies by device and setup. Pydroid 3 is usually easier.

1. Install Termux.
2. Update packages:
   ```bash
   pkg update && pkg upgrade
   ```
3. Install Python tools:
   ```bash
   pkg install python git
   ```
4. Clone/copy the project and enter it.
5. Install Kivy (may require additional system packages depending on device):
   ```bash
   pip install kivy
   ```
6. Run:
   ```bash
   python main.py
   ```

## Prepare APK (Buildozer on Linux)

Use this if you want to install the app like a regular Android app (APK):

1. Install system tools (Ubuntu/Debian example):
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config
   pip install --upgrade buildozer cython
   ```
2. From project root, build debug APK:
   ```bash
   buildozer android debug
   ```
3. APK output is typically in `bin/`.
4. Copy APK to phone and install (enable unknown sources if needed).

`buildozer.spec` is already included and preconfigured for this MVP.


## GitHub Website Preview (GitHub Pages)

This repo now includes `index.html` + `style.css` so you can preview the project as a website on GitHub.

1. Push your branch to GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Choose branch `main` and folder `/ (root)`.
5. Save and wait 1-2 minutes.
6. Open: `https://<your-username>.github.io/<repo-name>/`

> This website is a project preview page. The actual Kivy app still runs locally or as an APK.

## Notes for Next Phases

Planned in later phases:
- Dashboard analytics
- Voice assistant commands
- Timed reminder notifications and re-notify logic
- Goals tracker and motivation system
