FROM python:3.7.0-alpine
COPY docker/requirements.txt /srv/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /srv

RUN pip install --upgrade pip
RUN apk update
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN apk add jpeg-dev zlib-dev py-pillow
RUN apk add postgresql-dev
RUN apk add --no-cache libffi-dev
RUN pip install -r /srv/requirements.txt
