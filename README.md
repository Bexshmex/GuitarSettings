# ToneVault

ToneVault is my Django project for saving and sharing guitar amp presets.

The idea is simple: a user can choose a band and song, add the amp model, and
save settings like gain, bass, mid, treble, and reverb. Users can also upload an
audio demo and download a preset as a text file.

## Main Features

- User registration and login
- List of guitar presets
- Filter presets by band
- Add new presets when logged in
- Preset detail page
- Download preset settings as `.txt`
- Demo data command

## How to Run

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000
```

To add demo data:

```bash
docker compose run web python manage.py seed_data
```

Demo login:

```text
username: demo
password: demo12345
```

## About

I made this project to practice Django models, views, templates, forms,
authentication, file uploads, and basic Docker setup.
