# Week 10 will extend this with the serve extra and model weights.
FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY configs ./configs
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["vlmfw"]
CMD ["--help"]
