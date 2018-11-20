FROM python:3.7.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /srv/app
WORKDIR /srv/app

RUN pip install --upgrade pip
COPY Pipfile /srv/app/Pipfile

RUN pip install pipenv
RUN apk update \
	&& apk add --virtual build-deps gcc python3-dev musl-dev \
	&& apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
	&& apk add jpeg-dev zlib-dev py-pillow \
	&& apk add postgresql-dev \
	&& pipenv install --skip-lock --system

