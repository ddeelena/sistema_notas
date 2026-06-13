FROM python:3.14-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --dev

COPY . .

ENV PYTHONPATH=/app/src

EXPOSE 5000

CMD ["uv", "run", "python", "-m", "sistema_notas.app"]