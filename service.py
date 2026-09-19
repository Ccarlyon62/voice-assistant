import time
import os
from android.runnable import Runnable
from jnius import autoclass

# Prevent Android from killing the process when the screen turns off
PowerManager = autoclass('android.os.PowerManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

print("Voice Assistant Background Service Starting...")

def run_assistant_loop():
    while True:
        print("Assistant service active...")
        time.sleep(5)

if __name__ == '__main__':
    run_assistant_loop()

