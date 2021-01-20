#pull base image
FROM python:3.8

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set work directory
WORKDIR /src

# Install dependecies
COPY requirements.txt /src/
RUN pip install -r requirements.txt

# Copy project
COPY . /src/

