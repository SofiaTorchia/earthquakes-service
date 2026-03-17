IMAGE_NAME = userapi_dbimage
CONTAINER_NAME = userapi_dbcontainer
PORT = 5432

.PHONY: all
all: start_db run

.PHONY: start_db
start_db:
	podman build -t $(IMAGE_NAME) .
	podman run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME) \
        || podman start $(CONTAINER_NAME)

.PHONY: run
run:
	uv run db_init.py
	uv run fastapi dev main.py

.PHONY: clean
clean:
	podman stop $(CONTAINER_NAME)



