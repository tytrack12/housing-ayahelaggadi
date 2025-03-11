FROM python:3.10-slim

RUN pip install --upgrade pip
RUN pip install poetry==1.4.2

RUN useradd -ms /bin/bash appuser

RUN mkdir -p /home/appuser/app

RUN chown -R appuser:appuser /home/appuser

USER appuser

WORKDIR /home/appuser/app

ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

COPY --chown=appuser:appuser pyproject.toml poetry.lock* ./

RUN poetry install --no-dev

COPY --chown=appuser:appuser . .

CMD ["poetry", "run", "python", "train.py"]
