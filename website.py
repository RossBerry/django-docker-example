"""
website.py

Contains commands for managing a postgres db and django website running
in docker containers.

"""

import datetime
import os
import socket
import sys
import time


def get_latest_backup():
    """
    Retrieve name of latest postgres db backup file from ./postgres_data directory.
    """
    backups = [file for file in os.listdir(
        "./postgres_data") if len(file) >= 4 and ".sql" in file]
    if backups:
        return backups[-1]


def backup_db():
    """
    Backup postgres database.
    """
    print("Backing up website!")
    dt = datetime.datetime.now()
    db_backup_file = f"dump_{dt.date().day}-{dt.date().month}-{dt.date().year}\
             _{dt.time().hour}_{dt.time().minute}_{dt.time().second}.sql"
    os.system(f"docker exec -t postgres_db pg_dumpall -c -U postgres > ./postgres_data/{db_backup_file}")
    print(f"Database saved to {db_backup_file}")


def restore_db():
    """
    Restore database from latest backup file if available.
    """
    backup = get_latest_backup()
    if backup:
        print(f"Restoring from ./postgres_data/{backup}")
        os.system(
            f'cat ./postgres_data/{backup} | docker exec -i postgres_db psql -U postgres')
    else:
        print("Cannot find latest backup to restore from")


def start():
    """
    Start the website.
    """
    os.system("docker-compose up -d")
    # wait until postgres database port is available
    while not check_port(5432):
        pass
    time.sleep(5)  # wait for database to finish startup
    restore_db()


def save_stop():
    """
    Backup the website before shutting down the database and webserver.
    """
    backup_db()
    stop()


def stop():
    """
    Shutdown the postgres database and webserver.
    """
    print("Shutting down website!")
    os.system("docker-compose down")


def build():
    """
    Start the website with a new build.
    """
    os.system("docker-compose up -d --build")
    # wait until postgres database port is available
    while not check_port(5432):
        pass
    time.sleep(5)  # wait for database to finish startup
    restore_db()


def check_port(port):
    """
    Check if a port is open.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    port_open = True if result == 0 else False
    sock.close()
    return port_open


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
