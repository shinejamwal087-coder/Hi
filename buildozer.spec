[app]

title = Daily Utility App
package.name = dailyutility
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,md
source.exclude_dirs = .git,__pycache__,.venv,venv,build,dist

version = 0.1.0

requirements = python3,kivy,sqlite3

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = VIBRATE

# Keep build lightweight for low-end devices
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
