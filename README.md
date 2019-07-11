# Django-Docker Blog Example

A django blog website that launches in a docker container and uses a postgres database running in a separate docker container.

## Requirements
 - python 3.6+
 - docker
 - docker-compose

## Instructions:
- Starting website:
    ```
    python website.py start
    ```
- Stoping website:
    ```
    python website.py stop
    ```
- Rebuild and start website:
    ```
    python website.py build
    ```
- Backup and stop website:
    ```
    python website.py save_stop
    ```
- Backup database:
    ```
    python website.py backup_db
    ```
- Restore database:
    ```
    python website.py restore_db
    ```
- Create django admin super user:
    ```
    python website.py create_super_user
    ```
