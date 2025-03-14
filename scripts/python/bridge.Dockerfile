FROM python:3.7.10-slim-buster as builder
RUN groupadd -r mantik-bridge && useradd -r -g mantik-bridge mantik-bridge

# Install poetry for Python
ARG POETRY_VERSION="1.1.6"

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=$POETRY_VERSION \
  POETRY_HOME=/opt/poetry \
  POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update && apt-get install -y curl && \
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && \
  python -m venv /venv

ADD --chown=mantik-bridge:mantik-bridge target /opt/bridge
# TODO (fe): include data dir only for production example,
# delete upon availability of DataSet bridge
#ADD --chown=mantik-bridge:mantik-bridge data /opt/data

# Install bridge dependencies
WORKDIR /opt/bridge
RUN . /venv/bin/activate && poetry install --no-dev --no-root

# Killing Python Cache
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf && \
  cd /venv && \
  find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

RUN echo ". /venv/bin/activate && python main.py" > /opt/bridge/entrypoint.sh


FROM python:3.7.10-slim-buster
RUN groupadd -r mantik-bridge && useradd -r -g mantik-bridge mantik-bridge

COPY --from=builder /venv /venv
COPY --from=builder /opt/bridge /opt/bridge
# TODO (fe): delete upon availability of DataSet/Format bridge
#COPY --from=builder /opt/data /opt/data

USER mantik-bridge:mantik-bridge
WORKDIR /opt/bridge

EXPOSE 8502
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
