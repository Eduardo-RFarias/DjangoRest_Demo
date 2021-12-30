# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install psycopg2
RUN pip install psycopg2

# Install PipEnv
RUN pip install pipenv

# Copying the project to /app and setting the WORKDIR
WORKDIR /app
COPY . /app

# Install dependencies
RUN pipenv install --system

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Run gunicorn
CMD gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
