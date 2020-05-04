# convert your program to exe file
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "MyTunes",  # name you want to have of your app
        version = "0.1",
        description = "Music App!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("MyTune.py", base=base)]) # your .py file name
