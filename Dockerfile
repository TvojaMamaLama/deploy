#FROM tvoyamamalama/pylinux
FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev

ENV DJANGO_SETTINGS_MODULE=config.settings \
    DJANGO_ALLOW_ASYNC_UNSAFE=True

ADD requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /srv

ADD src /srv

RUN python manage.py migrate && python manage.py collectstatic --noinput #docker run -p 6379:6379 -d redis:5

CMD gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT