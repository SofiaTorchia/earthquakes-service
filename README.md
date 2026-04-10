[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains a FastAPI backend and a Streamlit frontend. The application retrieves earthquake data from https://earthquake.usgs.gov and displays earthquake locations on a world map for a selected start and end date.

**Steps to run the app**

- Install uv: https://docs.astral.sh/uv/getting-started/installation/
- start db

```
podman build -t earthquakes_dbimage backend/.
podman run -d -p 5432:5432 --name earthquakes_dbcontainer earthquakes_dbimage || podman start earthquakes_dbcontainer
```

- Start the backend with: ```make backend```
- Start the frontend with: ```make frontend```

http://127.0.0.1:8000/earthquakes?format=geojson&starttime=01-01-2024&endtime=01-02-2024&limit=10
