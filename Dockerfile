FROM python:3.14-slim-bookworm
ENV POETRY_VERSION=2.1.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR=/app-v/.cache/pypoetry
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update && apt-get install -y curl && \
    apt-get install -y git && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        g++ \
        gcc \
        python3-dev \
        gdal-bin libgdal-dev && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /tmp/src
RUN mv /tmp/src/* . \
    && DPNK_SECRET_KEY="fake_key" DPNK_DEBUG_TOOLBAR=True DPNK_SILK=True poetry run python manage.py compilemessages \
    && DPNK_SECRET_KEY="fake_key" DPNK_DEBUG_TOOLBAR=True DPNK_SILK=True poetry run python manage.py collectstatic --noinput \
    && mkdir media logs -p \
    && chmod +x wsgi.py
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
