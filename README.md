# Flask Task API — CI/CD Pipeline with Jenkins & Docker

A REST API with a fully automated CI/CD pipeline: every commit is linted,
tested, containerized, pushed to Docker Hub, and deployed — end to end, no
manual steps.

## Pipeline overview

```
git push
   │
   ▼
[Checkout]  →  [Lint]  →  [Test]  →  [Build]  →  [Push to Docker Hub]  →  [Deploy]
                flake8     pytest    docker      docker push              docker run
                            (8 tests)  build
```

Each stage gates the next — a lint failure stops the build before a single
test runs; a failing test blocks the image from ever being built or pushed.
Credentials (Docker Hub) are injected securely via Jenkins' credentials
store and never appear in source control or logs.

## Screenshot

*(Add a screenshot of a green Jenkins pipeline run here — see checklist below)*

## Tech stack

- **App**: Python, Flask
- **Testing**: pytest (8 unit tests covering all endpoints, including edge cases)
- **Linting**: flake8
- **Containerization**: Docker (multi-layer caching, non-root user, gunicorn WSGI server)
- **CI/CD**: Jenkins (declarative pipeline, native install)
- **Registry**: Docker Hub

## The app

A task management REST API:

| Method | Route                  | Description        |
|--------|-------------------------|---------------------|
| GET    | `/health`               | Health check        |
| GET    | `/tasks`                | List all tasks      |
| POST   | `/tasks`                | Create a task       |
| GET    | `/tasks/<id>`           | Get one task        |
| PATCH  | `/tasks/<id>/complete`  | Mark a task done    |
| DELETE | `/tasks/<id>`           | Delete a task       |

## Running it yourself

**Locally, without Docker:**
```bash
pip install -r requirements-dev.txt
python -m app.main
```

**With Docker:**
```bash
docker build -t task-api .
docker run -p 5000:5000 task-api
```

**Full pipeline (Jenkins):**
1. Install Jenkins natively or via Docker
2. Install Python 3, `python3-venv`, and the Docker CLI on the Jenkins host/agent
3. Add a Docker Hub access token as a Jenkins credential with ID `dockerhub-credentials`
4. Create a Pipeline job pointing at this repo, using the `Jenkinsfile` from SCM
5. Trigger a build

## What this project demonstrates

- A complete CI/CD pipeline built and debugged from scratch, including
  standing up and configuring the CI server itself (not just writing YAML
  for a hosted service)
- Gated, sequential pipeline stages with fail-fast behavior
- Secure credential handling (Jenkins credentials store, `--password-stdin`,
  no secrets in source control)
- Idempotent deployment (safely re-runnable without manual cleanup)
- Container security basics: non-root user, minimal base image, production
  WSGI server instead of a dev server
- Real debugging experience: missing system packages, Docker-outside-of-Docker
  permissions, native vs. containerized Jenkins tooling differences

## Possible extensions

- Add branch protection and run the pipeline on pull requests before merge
- Move the app to a proper database instead of in-memory storage
- Add a staging environment with manual approval before production deploy
- Deploy to Kubernetes instead of a single `docker run`
