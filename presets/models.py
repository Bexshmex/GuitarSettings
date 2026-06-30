from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Band(models.Model):
    # a band
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Preset(models.Model):
    # an amp preset
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=200)
    amp_model = models.CharField(max_length=120)

    gain = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    bass = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    mid = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    treble = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    reverb = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    audio_demo = models.FileField(upload_to='demos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.song_name} ({self.amp_model})'

    def get_absolute_url(self):
        return reverse('preset_detail', args=[self.pk])
