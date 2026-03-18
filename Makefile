.PHONY: backend
backend: 
	uv run fastapi dev backend/api.py 

.PHONY: frontend
frontend: 
	uv run streamlit run frontend/dashboard.py
