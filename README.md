# FastAPI DevOps Workflow

A minimal FastAPI app used as a learning sandbox for building a CI/CD pipeline
from scratch. The application code is intentionally small — the real point of
this repo is the automation (linting, testing, CI, Docker) built around it.

## Project goal

Learn and practice a typical Python DevOps pipeline, step by step:

1. ~~Simple FastAPI app with a couple of endpoints~~
2. ~~Local tooling: `uv` for dependency management, `ruff` for linting/formatting~~
3. Basic test suite with `pytest` + `httpx`
4. GitHub Actions workflow (`ci.yaml`) running `uv sync`, `ruff check`, `pytest`
5. Docker, multi-stage builds, and pre-commit hooks

See [`task.md`](task.md) for the full blueprint and current progress.

## Stack

- **FastAPI** — web framework
- **uv** — dependency management and running the app
- **loguru** — application logging (with a handler that intercepts stdlib
  `logging` records so FastAPI/uvicorn logs share the same format)
- **ruff** — linting/formatting (via pre-commit)
- **pre-commit** — git hooks (`uv-lock`, `uv-sync`, `uv-export`)

## Requirements

- Python 3.12 (see `.python-version`)
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Running the app

```bash
uv run app/main.py
```

Or with uvicorn's reload for development:

```bash
uv run uvicorn app.main:app --reload
```

The app starts on `http://localhost:8000`.

## Endpoints

| Method | Path      | Description                  |
|--------|-----------|-------------------------------|
| GET    | `/`       | Returns `{"Hello": "World"}` |
| GET    | `/health` | Returns `{"status": "healthy"}` |

## Logging

Logging is configured in `app/loguru_handler.py` and wired up on startup in
`app/main.py`. Logs go to both stdout and a rotating `file.log` file
(10 MB rotation, 7 day retention, zipped). Standard library logging (used by
uvicorn/FastAPI internally) is intercepted and routed through loguru so all
log output shares one format.

## Pre-commit hooks

```bash
uv run pre-commit install
```

This installs hooks that keep `uv.lock` and the exported requirements in sync
on commit, checkout, merge, and rewrite.

## Status

No CI workflow or test suite exists yet — those are the next steps in the
blueprint (see `task.md`).
