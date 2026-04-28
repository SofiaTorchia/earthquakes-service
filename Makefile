.PHONY: backend
backend: 
	uv run fastapi dev backend/api/api.py 

.PHONY: frontend
frontend: 
	uv run streamlit run frontend/dashboard.py

.PHONY: pylint
pylint: 
	uv run pylint frontend/dashboard.py
	uv run pylint backend/api/api.py 

.PHONY: mypy
mypy: 
	uv run mypy frontend/dashboard.py
	uv run mypy backend/api/api.py 

.PHONY: black
black: 
	uv run black frontend/dashboard.py
	uv run black backend/api/api.py 

.PHONY: clean
clean: black mypy pylint

.PHONY: db_init
db_init: 
	podman build -t earthquakes-db:latest backend/.
	podman run -d -p 5432:5432 --name earthquakes_dbcontainer earthquakes-db:latest || podman start earthquakes_dbcontainer
	uv run python backend/pipeline/db_init.py

.PHONY: db_update
db_update: 
	uv run python backend/pipeline/db_update.py

.PHONY: api_init
api_init:
	podman build -t earthquakes-api:latest .
	podman run -d -p 8000:8000 --name earthquakes_apicontainer earthquakes-api:latest || podman start earthquakes_apicontainer