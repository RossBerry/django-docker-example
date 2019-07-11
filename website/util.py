import sys
import time


def handle_args(in_argv):
    length = len(in_argv)
    if length == 1:
        print(MESSAGES["info"])
    elif in_argv[1] in COMMANDS:
        command = in_argv[1]
        options = in_argv[2:] if length > 2 else []
        COMMANDS[command](options)
    else:
        print(MESSAGES["invalid"])

def wait(options):
    seconds = int(options[0])
    time.sleep(seconds)


PLATFORM = sys.platform
if PLATFORM == "linux" or PLATFORM == "linux2":
    PLATFORM = "lnx"
elif PLATFORM == "darwin":
    PLATFORM = "osx"
elif PLATFORM == "win32":
    PLATFORM = "win"

if __name__ == "__main__":
    MESSAGES = {
        "info": "list commands",
        "invalid": "not a valid command",
        "start": "Starting the website{}!"
    }
    COMMANDS = {
        "wait": wait
    }
    handle_args(sys.argv)
