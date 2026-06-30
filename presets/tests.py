from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Band, Preset


class PresetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pw12345!')
        self.band = Band.objects.create(name='Metallica')
        self.preset = Preset.objects.create(
            author=self.user, band=self.band,
            song_name='Enter Sandman', amp_model='Mesa Boogie',
            gain=8, bass=6, mid=5, treble=7, reverb=3,
        )

    # 1. upload with audio demo
    def test_upload_audio_demo(self):
        self.client.login(username='alice', password='pw12345!')
        audio = SimpleUploadedFile('demo.mp3', b'fake audio', content_type='audio/mpeg')
        response = self.client.post(reverse('preset_create'), {
            'band': self.band.id,
            'song_name': 'Master of Puppets',
            'amp_model': 'JCM800',
            'gain': 9, 'bass': 7, 'mid': 6, 'treble': 8, 'reverb': 2,
            'audio_demo': audio,
        })
        self.assertEqual(response.status_code, 302)
        created = Preset.objects.get(song_name='Master of Puppets')
        self.assertEqual(created.author, self.user)
        self.assertTrue(created.audio_demo)

    # 2. json endpoint
    def test_json_endpoint(self):
        response = self.client.get(reverse('presets_json'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['presets']), 1)
        self.assertEqual(data['presets'][0]['song_name'], 'Enter Sandman')

    # 3. anonymous redirected to login
    def test_anonymous_redirected(self):
        response = self.client.get(reverse('preset_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])
