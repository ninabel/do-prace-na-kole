FROM python:3.14-slim-bookworm
ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/opt/.cache/pypoetry
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update && apt-get install -y curl && \
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
