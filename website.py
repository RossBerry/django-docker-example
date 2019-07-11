#!/usr/bin/env python
"""
website.py

Contains command functions for managing a postgres db and django website running
inside docker containers.

"""
import datetime
import os
import socket
import sys
import time


def build(options):
    """
    Starts the website with a new build.
    """
    print("Building the website!")
    options_str = " " + " ".join(options) if options else ""
    build_cmd = f"docker-compose up{options_str} --build"
    send_command(build_cmd)


def check_port(port):
    """
    Checks if a port is open.
    """
    try_count = 0
    port_open = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while try_count < 100:
        result = sock.connect_ex(('127.0.0.1', port))
        if result:
            port_open = True
            break
        time.sleep(1)
        try_count += 1
    sock.close()
    return port_open


def create_super_user():
    """
    Create super user account for django website.
    """
    create_super_user_cmd = "docker-compose run website python manage.py createsuperuser"
    send_command(create_super_user_cmd)


def get_latest_backup():
    """
    Retrieves the name of latest postgres db backup file.
    """
    if "postgres_data" in os.listdir("./"):
        backups = [file for file in os.listdir(
            "./postgres_data") if len(file) >= 4 and ".sql" in file]
        if backups:
            return backups[-1]


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


def restart(options):
    """
    Restarts the website.
    """
    stop([option for option in options if option != "-r"])
    start([option for option in options if option != "-s"])


def restore():
    """
    Restore the website.
    """
    restore_db()


def restore_db():
    """
    Restores database from latest backup file, if available.
    """
    latest_backup = get_latest_backup()
    if latest_backup:
        print(f"Restoring from {latest_backup}")
        db_restore_cmd = f"cat ./postgres_data/{latest_backup} | docker exec -i postgres_db psql -U postgres"
        send_command(db_restore_cmd)
    else:
        print("No backup file to restore from!")

def save():
    """
    Saves the website.
    """
    save_db()


def save_db():
    """
    Saves the postgres database.
    """
    print("Saving the database!")
    if "postgres_data" not in os.listdir("./"):
        print("postgres_data directory does not already exist!")
        print("creating postgres_data directory for db backup storage")
        send_command("mkdir postgres_data")
    dt = datetime.datetime.now()
    db_backup_file = f"dump_{dt.date().day}-{dt.date().month}-{dt.date().year}_{dt.time().hour}_{dt.time().minute}_{dt.time().second}.sql"
    db_backup_cmd = f"docker exec -t postgres_db pg_dumpall -c -U postgres > ./postgres_data/{db_backup_file}"
    send_command(db_backup_cmd)
    print(f"Database saved to {db_backup_file}")

def send_command(command):
    """
    Sends a command to the command line.
    """
    try:
        if PLATFORM == "win" or PLATFORM == "osx":
            os.system(command)
        elif PLATFORM == "lnx":
            os.system(f"sudo {command}")
    except(KeyboardInterrupt):
        print("Website stopped!")


def start(options):
    """
    Starts the website.
    """
    msg = MESSAGES["start"]
    msg = msg.format(" in detached mode") if "-d" in options else msg.format("")
    print(msg)
    restore_option = "-r" in options
    if restore_option:
        options.remove("-r")
    options_str = " " + " ".join(options) if options else ""
    start_cmd = f"docker-compose up{options_str}"
    send_command(start_cmd)
    if restore_option:
        restore()


def stop(options):
    """
    Shuts down the postgres database and webserver.
    """
    print("Stopping website and database!")
    save_option = "-s" in options
    if save_option:
        options.remove("-s")
        save()
    options_str = " " + " ".join(options) if options else ""
    stop_cmd = f"docker-compose down{options_str}"
    send_command(stop_cmd)


def wait(seconds):
    """
    Wait for a specified number of seconds.
    """
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
        "build": build,
        "create_super_user": create_super_user,
        "restart": restart,
        "restore": restore,
        "save": save,
        "start": start,
        "stop": stop,
        "wait": wait
    }
    handle_args(sys.argv)
