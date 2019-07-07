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


def backup_db():
    """
    Backs up the postgres database.
    """
    print("Backing up website!")
    if "postgres_data" not in os.listdir("./"):
        print("postgres_data directory does not already exist!")
        print("creating postgres_data directory for db backup storage")
        send_command("mkdir postgres_data")
    dt = datetime.datetime.now()
    db_backup_file = f"dump_{dt.date().day}-{dt.date().month}-{dt.date().year}_{dt.time().hour}_{dt.time().minute}_{dt.time().second}.sql"
    db_backup_cmd = f"docker exec -t postgres_db pg_dumpall -c -U postgres > ./postgres_data/{db_backup_file}"
    send_command(db_backup_cmd)
    print(f"Database saved to {db_backup_file}")

def build():
    """
    Starts the website with a new build.
    """
    build_cmd = "docker-compose up --build"
    send_command(build_cmd)

    def build_d():
        """
    Starts the website with a new build - runs in the background.
    """
    build_cmd = "docker-compose up -d --build"
    send_command(build_cmd)

    def build_restore():
        """
    Starts the website with a new build and restores the latest db backup.
    """
    build_d()
    # wait until postgres database port is available
    while not check_port(5432):
        pass
    time.sleep(10)  # wait for database to finish startup
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

def restore_db():
    """
    Restores database from latest backup file, if available.
    """
    backup = get_latest_backup()
    if backup:
        print(f"Restoring from {backup}")
        db_restore_cmd = f"cat ./postgres_data/{backup} | docker exec -i postgres_db psql -U postgres"
        send_command(db_restore_cmd)
    else:
        print("Cannot find a backup file to restore from")

def save_stop():
    """
    Backs up the website, then shuts down the database and webserver.
    """
    backup_db()
    stop()

def send_command(command):
    """
    Sends a command to the command line.
    """
    if PLATFORM == "win" or PLATFORM == "osx":
        os.system(command)
    elif PLATFORM == "lnx":
        os.system(f"sudo {command}")

def start():
    """
    Starts the website.
    """
    print("Starting the website!")
    start_cmd = "docker-compose up"
    send_command(start_cmd)

def start_d():
    """
    Starts the website as a daemon.
    """
    print("Starting the website!")
    start_cmd = "docker-compose up -d"
    send_command(start_cmd)

def start_restore():
    """
    Starts the website and restore the latest db backup.
    """
    start_d()
    # wait until postgres database port is available
    while not check_port(5432):
        pass
    time.sleep(10)  # wait for database to finish startup
    restore_db()

def stop():
    """
    Shuts down the postgres database and webserver.
    """
    print("Shutting down website!")
    stop_cmd = "docker-compose down"
    send_command(stop_cmd)

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
        "build_d",
        "build_restore",
        "create_super_user",
        "restore_db",
        "save_stop",
        "start",
        "start_d",
        "start_restore",
        "stop"
    ]

    if sys.argv[1] in COMMANDS:
        eval(f'{sys.argv[1]}()')
