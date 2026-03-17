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

- uv installed
- FastAPI development tools installed

## To do

- [ ] New readme
- [ ] Use a build tool (uv)
- [ ] Point stramlit app to fastapi app