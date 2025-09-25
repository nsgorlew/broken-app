This app uses the following stack: Nginx, Gunicorn, FastAPI

-The application runs in a Docker container
-Nginx acts as a reverse proxy and distributes requests to Gunicorn workers
-Each Gunicorn worker is a process running the FastAPI application

