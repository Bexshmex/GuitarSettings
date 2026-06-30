from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from presets.models import Band, Preset

BANDS = ['Linkin Park', 'Metallica', 'Nirvana']

PRESETS = [
    ('Metallica', 'Enter Sandman', 'Mesa Boogie Mark IV', 8, 6, 5, 7, 3),
    ('Metallica', 'Master of Puppets', 'Marshall JCM800', 9, 7, 6, 8, 2),
    ('Linkin Park', 'Numb', 'PRS Archon', 7, 5, 6, 6, 4),
    ('Linkin Park', 'In the End', 'Mesa Triple Rectifier', 6, 5, 5, 6, 5),
    ('Nirvana', 'Smells Like Teen Spirit', 'Fender Bassman', 7, 6, 4, 6, 6),
]


class Command(BaseCommand):
    help = 'Populate the database with sample bands and presets.'

    def handle(self, *args, **options):
        author, created = User.objects.get_or_create(username='demo')
        if created:
            author.set_password('demo12345')
            author.save()
            self.stdout.write('Created demo user (login: demo / demo12345).')

        bands = {
            name: Band.objects.get_or_create(name=name)[0] for name in BANDS
        }

        added = 0
        for band_name, song, amp, gain, bass, mid, treble, reverb in PRESETS:
            _, was_created = Preset.objects.get_or_create(
                band=bands[band_name], song_name=song,
                defaults={
                    'author': author, 'amp_model': amp,
                    'gain': gain, 'bass': bass, 'mid': mid,
                    'treble': treble, 'reverb': reverb,
                },
            )
            added += int(was_created)

        self.stdout.write(
            f'Seed complete: {len(bands)} bands, {added} new presets added.'
        )
