.PHONY: backend
backend: 
	uv run fastapi dev backend/api.py 

.PHONY: frontend
frontend: 
	uv run streamlit run frontend/dashboard.py

.PHONY: pylint
pylint: 
	uv run pylint frontend/dashboard.py
	uv run pylint backend/api.py 

.PHONY: mypy
mypy: 
	uv run mypy frontend/dashboard.py
	uv run mypy backend/api.py 

.PHONY: black
black: 
	uv run black frontend/dashboard.py
	uv run black backend/api.py 

.PHONY: clean
clean: black mypy pylint
