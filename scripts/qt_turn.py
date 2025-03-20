import subprocess

subprocess.run(["pyside6-uic", "./scrcpy_ui/add_deivce.ui", "-o", "./scrcpy_ui/ui_add_device.py"])
subprocess.run(["pyside6-uic", "./scrcpy_ui/main.ui", "-o", "./scrcpy_ui/ui_main.py"])
