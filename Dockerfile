FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# collect static files into the image so WhiteNoise can serve them
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "tonevault.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
