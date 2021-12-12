FROM python:3
COPY script.py /script.py
CMD ["python", "/script.py"]

FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app