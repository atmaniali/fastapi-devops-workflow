# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

A self-training project to learn how to build a CI/CD pipeline around a
Python web app. The FastAPI application itself is deliberately minimal and
is **not** the point — it exists only as something to attach tooling to.
Do not add application features, endpoints, or business logic unless
explicitly asked; the focus of this repo is the automation around the code
(linting, testing, CI, Docker), not the app itself.

The intended learning path is laid out in `task.md`:

1. Simple FastAPI app (done)
2. Local tooling: `uv` + `ruff` + pre-commit (done)
3. `pytest` + `httpx` test suite (not started)
4. GitHub Actions `ci.yaml` running `uv sync`, `ruff check`, `pytest` (not started)
5. Docker / multi-stage builds on top of the working pipeline (not started)

When asked to "move the pipeline forward," check this list and `task.md`
before assuming what's next — do the next unchecked step, not several at
once, unless asked.

## Environment

- OS: Windows. Use PowerShell syntax for shell commands, not bash/POSIX.
- Package manager: `uv`. Do not use bare `pip`/`python -m venv` — use `uv sync`,
  `uv add`, `uv run`.
- Python version is pinned via `.python-version` (3.12).

## Common commands

```powershell
uv sync                          # install/update the environment from uv.lock
uv run app/main.py               # run the app directly
uv run uvicorn app.main:app --reload   # run with autoreload
uv run pre-commit install        # install git hooks
uv run pre-commit run --all-files
```

There is no test runner configured yet (`pytest` is not a dependency). When
adding the test suite (step 3 of the blueprint), add `pytest` and `httpx` as
dev dependencies via `uv add --dev`, not by hand-editing `pyproject.toml`.

## Code layout

- `app/main.py` — FastAPI app, routes, startup logging config.
- `app/loguru_handler.py` — `InterceptHandler`, bridges stdlib `logging`
  records (from FastAPI/uvicorn) into loguru so all logs share one format.
- `docs/source.md` — personal reference links for topics being learned
  (logging, CI, pre-commit, project structure, SQLModel). Not user-facing
  docs; don't restructure it into something else.
- `task.md` — the step-by-step blueprint driving this project. Gitignored
  from a docs standpoint conceptually but currently tracked; treat it as the
  source of truth for "what's next," and keep it updated if the user
  completes a step.
- `file.log` — runtime log output (rotated by loguru). Not source; don't
  edit it, and don't worry about its contents in reviews.

## Conventions already in place — keep following them

- Logging goes through `loguru`, configured once in `configure_logging()` in
  `app/main.py`, called from a startup event. Don't introduce a second
  logging setup path (e.g. stdlib `logging.basicConfig` directly in route
  code) — route everything through the existing loguru setup.
- `ruff` is the formatter/linter of record (enforced via pre-commit). Don't
  introduce black/flake8/isort configs alongside it.
- Dependencies are managed exclusively through `uv` / `pyproject.toml` /
  `uv.lock`. Never edit `uv.lock` by hand.

## What not to do

- Don't scaffold a full production-grade FastAPI project structure (routers/
  services/models/config layers) — this app is meant to stay small; the
  complexity belongs in the pipeline, not the app.
- Don't add a Dockerfile or GitHub Actions workflow preemptively unless the
  user asks for that specific blueprint step — they're learning each stage
  deliberately, one at a time.
- Don't remove or "clean up" `task.md` or `docs/source.md` — they're the
  user's own working notes, not generated artifacts.
