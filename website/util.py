import sys
import time

def wait(seconds):
    time.sleep(seconds)

PLATFORM = sys.platform
if PLATFORM == "linux" or PLATFORM == "linux2":
    PLATFORM = "lnx"
elif PLATFORM == "darwin":
    PLATFORM = "osx"
elif PLATFORM == "win32":
    PLATFORM = "win"

if __name__ == "__main__":
    COMMANDS = [
        "wait"
    ]
    
    if sys.argv[1] in COMMANDS:
        if sys.argv[1] != "wait":
            eval(f'{sys.argv[1]}()')
        elif len(sys.argv) == 3:
            eval(f'{sys.argv[1]}({sys.argv[2]})')