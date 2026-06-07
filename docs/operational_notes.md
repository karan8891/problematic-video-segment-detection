# Operational Notes

## Logging

The application logs processing status transitions:

queued
processing
completed
failed

## Failure Handling

If media extraction fails:

- Processing does not terminate.
- A fallback transcript path is used.
- The report remains available.

## Storage

Videos:

data/videos/

Artifacts:

data/artifacts/

SQLite Database:

data/app.db

## Monitoring Opportunities

Future improvements:

- Structured logging
- OpenTelemetry
- Prometheus
- Grafana

## Scalability

Prototype:
FastAPI + BackgroundTasks

Production:
FastAPI + Celery + Redis + PostgreSQL

## Security Considerations

- Input validation
- URL validation
- Error isolation
- Background processing separation