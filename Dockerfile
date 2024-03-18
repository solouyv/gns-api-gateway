FROM python:3.9-slim

ENV PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    LC_ALL=C \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/code/.venv \
    PYTHONPATH="$PYTHONPATH:/code" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"
ENV PATH="$VENV_PATH/bin:$POETRY_PATH/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl \
    build-essential && \
    pip install pip==23.2.1 && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_PATH python3 - && \
    poetry --version && \
    poetry config virtualenvs.in-project true && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code/

COPY pyproject.toml poetry.lock* /code/

RUN poetry install --no-interaction --no-ansi --no-root

COPY . /code

EXPOSE 8000

CMD ["python", "-m", "gns_api_gateway", "serve"]
