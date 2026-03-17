## Development workflow

This project uses a Makefile to automate starting the Postgres database container and running the FastAPI development server.

**Available commands**

- ```make``` <br>
    Runs the full workflow: builds the database image, starts (or restarts) the Postgres container, initializes the database, and launches the FastAPI development server.

- ```make start_db``` <br>
Builds the Podman image defined in the Dockerfile and starts the Postgres container. If the container already exists, it is started instead of recreated.

- ```make run``` <br>
Initializes the database using db_init.py and starts the FastAPI development server using uv.

- ```make clean``` <br>
Stops the running Postgres container.

**Prerequisites**

- Podman installed and running
- uv installed
- FastAPI development tools installed

## To do

- [X] Dockerfile
- [ ] Start docker container with one command (makefile?)
- [ ] In the same makefile: run python script that runs sql query (psycopg)
- [X] Make queries idempotent
- [X] Read sql file from queries.py
- [X] Pass db connection settings as env var
- [ ] Use a build tool (uv)
- [ ] Point stramlit app to fastapi app
- [X] In db: how to use paramenters in psycopg connect
- [X] queries.py and queries.sql to get row from user id
- [X] Return Pydantic BaseModel instance as output of "get" 
function of FastAPI. A database row is transformed into a Pydantic Basemodel object instance.