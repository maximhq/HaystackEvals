FROM python:3.11.9@sha256:a03f4e5b67980d474839e7b4d4a405871a4259690287d65060cff95d0cb311cd AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
FROM python:3.11.9-slim@sha256:8fb099199b9f2d70342674bd9dbccd3ed03a258f26bbd1d556822c6dfc60c317
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
CMD ["/app/.venv/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]
