# ToneVault

ToneVault is my Django project for saving and sharing guitar amp presets.

The idea is simple: a user can choose a band and song, add the amp model, and
save settings like gain, bass, mid, treble, and reverb. Users can also upload an
audio demo and download a preset as a text file.

## Main Features

- User registration and login
- List of guitar presets
- Filter presets by band and text search
- Add, edit, and delete presets (author or superuser only)
- Preset detail page
- Download preset settings as `.txt`
- Demo data command

## Tech / Deployment Setup

- Django 5.2 served by **gunicorn**
- **PostgreSQL** in Docker (SQLite fallback for simple local usage)
- Static files served by **WhiteNoise**
- Configuration through environment variables

## How to Run (Docker Compose)

```bash
docker compose up --build
```

Then open <http://localhost:8000>.

Migrations run automatically when the `web` container starts.
To run them manually:

```bash
docker compose run --rm web python manage.py migrate
```

Create a superuser:

```bash
docker compose run --rm web python manage.py createsuperuser
```

Load demo data:

```bash
docker compose run --rm web python manage.py seed_data
```

Demo login after seeding:

```text
username: demo
password: demo12345
```

## Environment Variables

Copy `.env.example` to `.env` and adjust. `docker compose` picks it up
automatically; safe defaults are used if a variable is missing.

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key — set a real random value in production | insecure dev key |
| `DJANGO_DEBUG` | `True`/`False` | `True` locally, `False` in compose |
| `DJANGO_ALLOWED_HOSTS` | comma-separated hostnames | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | comma-separated origins for CSRF | `http://localhost:8000` in compose |
| `DJANGO_SECURE_SSL` | `True` enables SSL redirect, secure cookies, HSTS — only behind HTTPS | `False` |
| `DATABASE_URL` | PostgreSQL URL; unset = local SQLite | compose points it at the `db` service |

## Running Without Docker (simple local usage)

Recommended local Python version: **3.12** (same as the Docker image).

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Without `DATABASE_URL` the app uses a local `db.sqlite3` file.

## Notes

- Uploaded media is stored in a Docker volume (`media_data`) and served by
  Django itself — fine for this project; a real deployment would use nginx or
  object storage.
- Static files are collected into the image at build time and served by
  WhiteNoise.

## About

I made this project to practice Django models, views, templates, forms,
authentication, file uploads, and a production-style Docker setup.
