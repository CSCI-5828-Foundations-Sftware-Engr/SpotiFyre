
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV SPOTIPY_CLIENT_ID='3d7af19cb8f84dcab05b9f44feab935e'
ENV SPOTIPY_CLIENT_SECRET='e21a86202bc14a83a20f32c80e0d700b'
ENV SPOTIPY_REDIRECT_URI='http://localhost:8080/callback'
ENV SPOTIFY_SCOPE='user-read-recently-played user-library-read user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative'

# Install production dependencies.
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app
COPY . /app
ENV GOOGLE_APPLICATION_CREDENTIALS='/app/fse-new-faab077c290e.json'
EXPOSE 80
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :80  --workers 1 --threads 8 --timeout 0 __init__:create_app