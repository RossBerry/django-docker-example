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

def get_latest_backup():
    """
    Retrieves the name of latest postgres db backup file.
    """
    backups = [file for file in os.listdir(
        "./postgres_data") if len(file) >= 4 and ".sql" in file]
    if backups:
        return backups[-1]


def backup_db():
    """
    Backs up the postgres database.
    """
    print("Backing up website!")
    dt = datetime.datetime.now()
    db_backup_file = f"dump_{dt.date().day}-{dt.date().month}-{dt.date().year}\
             _{dt.time().hour}_{dt.time().minute}_{dt.time().second}.sql"
    db_backup_cmd = f"docker exec -t postgres_db pg_dumpall -c -U postgres > ./postgres_data/{db_backup_file}"
    send_command(db_backup_cmd)
    print(f"Database saved to {db_backup_file}")


def restore_db():
    """
    Restores database from latest backup file, if available.
    """
    backup = get_latest_backup()
    if backup:
        print(f"Restoring from ./postgres_data/{backup}")
        db_restore_cmd = f"cat ./postgres_data/{backup} | docker exec -i postgres_db psql -U postgres"
        send_command(db_restore_cmd)
    else:
        print("Cannot find a backup file to restore from")


def start():
    """
    Starts the website.
    """
    start_cmd = "docker-compose up -d"
    send_command(start_cmd)
    # wait until postgres database port is available
    while not check_port(5432):
        pass
    time.sleep(5)  # wait for database to finish startup
    restore_db()


def save_stop():
    """
    Backs up the website, then shuts down the database and webserver.
    """
    backup_db()
    stop()


def stop():
    """
    Shuts down the postgres database and webserver.
    """
    print("Shutting down website!")
    stop_cmd = "docker-compose down"
    send_command(stop_cmd)


def build():
    """
    Starts the website with a new build.
    """
    build_cmd = "docker-compose up -d --build"
    send_command(build_cmd)
    # wait until postgres database port is available
    while not check_port(5432):
        pass
    time.sleep(5)  # wait for database to finish startup
    restore_db()


def check_port(port):
    """
    Checks if a port is open.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    port_open = True if result == 0 else False
    sock.close()
    return port_open

def send_command(command):
    """
    Sends a command to the command line.
    """
    if PLATFORM == "win" or PLATFORM == "osx":
        os.system(command)
    elif PLATFORM == "lnx":
        os.system(f"sudo {command}")

PLATFORM = sys.platform
if PLATFORM == "linux" or PLATFORM == "linux2":
    PLATFORM = "lnx"
elif PLATFORM == "darwin":
    PLATFORM = "osx"
elif PLATFORM == "win32":
    PLATFORM = "win"

if __name__ == "__main__":
    COMMANDS = [
        "backup_db",
        "build",
        "restore_db",
        "save_stop",
        "start",
        "stop"
    ]

    if sys.argv[1] in COMMANDS:
        eval(f'{sys.argv[1]}()')
