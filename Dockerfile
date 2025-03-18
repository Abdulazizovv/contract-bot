# FROM python:3.11

# # Set the working directory
# WORKDIR /app

# # Copy and install dependencies
# COPY requirements.txt /usr/src/app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project files
# COPY . ./
# # COPY /usr/src/app/.env .env

# # Run migrations and start the Django bot
# # CMD ["sh", "-c", "python manage.py migrate && python manage.py app"]



FROM python:3.12.3-alpine


# RUN apk update \
#     && apk add --no-cache \
#     build-base \
#     mariadb-dev \
#     libffi-dev \
#     python3-dev \
#     && pip install --upgrade pip \
#     && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r\
    /usr/src/app/requirements.txt
    
COPY ./config /usr/src/app/