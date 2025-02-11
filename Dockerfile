FROM python:3.13-bullseye as builder

ARG POETRY_VERSION=2.0.1

RUN pip install poetry==${POETRY_VERSION}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root \
    && rm -rf $POETRY_CACHE_DIR



FROM python:3.13-slim-bullseye as runner

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

RUN adduser --disabled-password --gecos 'Django Runner' --uid 1000 django

COPY --from=builder --chown=django ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN mkdir -p /static /media \
    && chown -R django /static /media

COPY --chown=django . /app

WORKDIR /app
USER django
