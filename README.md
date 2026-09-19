<<<<<<< HEAD
# flask-jenkins-cicd-pipeline
=======
# CI/CD Pipeline — Flask Task API

![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci-cd.yml/badge.svg)

A small Flask REST API with a full CI/CD pipeline: every push is linted,
tested, containerized, and (on merge to `main`) pushed to Docker Hub as a
versioned image.

## Pipeline

```
push/PR to main
      |
      v
   [Lint]  --- flake8 style check
      |
      v
   [Test]  --- pytest, 8 unit tests
      |
      v
[Build & Push]  --- docker build -> push to Docker Hub (main branch only)
                     tagged :latest and :<commit-sha>
```

Each stage gates the next — a lint failure blocks tests, a test failure blocks
the build. The build/push stage only runs on `main`, so pull requests get
validated without publishing an image.

## The app

A minimal task API:

| Method | Route                     | Description          |
|--------|---------------------------|-----------------------|
| GET    | `/health`                 | Health check          |
| GET    | `/tasks`                  | List all tasks        |
| POST   | `/tasks`                  | Create a task         |
| GET    | `/tasks/<id>`             | Get one task          |
| PATCH  | `/tasks/<id>/complete`    | Mark a task done      |
| DELETE | `/tasks/<id>`             | Delete a task         |

The app itself is intentionally simple — the point of this project is the
pipeline around it, not the app's feature set.

## Running locally

```bash
pip install -r requirements-dev.txt
python -m app.main
# API now running on http://localhost:5000
```

## Running tests locally

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
flake8 app/ tests/ --max-line-length=100
```

## Running with Docker

```bash
docker build -t cicd-pipeline-project .
docker run -p 5000:5000 cicd-pipeline-project
```

## Setting up the pipeline on your own fork

1. Push this repo to your own GitHub account.
2. Create a [Docker Hub](https://hub.docker.com) account and an
   [access token](https://hub.docker.com/settings/security) (not your password).
3. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
   and add two repository secrets:
   - `DOCKERHUB_USERNAME` — your Docker Hub username
   - `DOCKERHUB_TOKEN` — the access token from step 2
4. Update the badge URL at the top of this README with your GitHub
   username/repo.
5. Push to `main` — the Actions tab will show the pipeline running, and a
   successful run will publish `<your-dockerhub-username>/cicd-pipeline-project`
   to Docker Hub.

## What this demonstrates

- Multi-stage pipeline with proper job dependencies (`needs:`)
- Conditional deployment (build/push only on `main`, not every PR)
- Docker layer caching in CI via GitHub Actions cache (`type=gha`)
- Immutable image tagging by commit SHA, alongside a floating `latest` tag
- Secrets management (no credentials in code)
- Non-root container user, production WSGI server (gunicorn) instead of
  Flask's dev server

## Possible extensions

- Add a `deploy` job that SSHes into an EC2 instance and pulls the new image
  (or deploys to Kubernetes/ECS)
- Add a code coverage report and upload it as a workflow artifact
- Add Dependabot for automated dependency updates
- Add a `staging` environment with manual approval before production deploy
>>>>>>> bd2d3e3 (Pushing code to GitHub)
