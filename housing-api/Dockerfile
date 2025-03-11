FROM python:3.10-slim


RUN pip install --upgrade pip


ENV POETRY_VERSION=1.4.2
RUN pip install poetry==$POETRY_VERSION

RUN useradd -ms /bin/bash appuser

USER appuser

WORKDIR /home/appuser/app

COPY --chown=appuser:appuser pyproject.toml poetry.lock* ./

RUN poetry install --no-dev

COPY --chown=appuser:appuser . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]