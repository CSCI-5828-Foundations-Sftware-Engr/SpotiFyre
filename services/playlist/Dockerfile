
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True


# Install production dependencies.
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ENV FLASK_APP=app
COPY . /playlist
ENV GOOGLE_APPLICATION_CREDENTIALS=

WORKDIR /playlist

# EXPOSE 80
CMD ["python", "subscriber.py"]
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :80  --workers 1 --threads 8 --timeout 0 __init__:create_app