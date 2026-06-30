from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Preset


class SignUpForm(UserCreationForm):
    # sign up form

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)


class PresetForm(forms.ModelForm):
    # preset form

    class Meta:
        model = Preset
        fields = (
            'band', 'song_name', 'amp_model',
            'gain', 'bass', 'mid', 'treble', 'reverb',
            'audio_demo',
        )
        widgets = {
            'band': forms.Select(attrs={'class': 'form-select'}),
            'song_name': forms.TextInput(attrs={'class': 'form-control'}),
            'amp_model': forms.TextInput(attrs={'class': 'form-control'}),
            'gain': forms.NumberInput(attrs={'class': 'form-control'}),
            'bass': forms.NumberInput(attrs={'class': 'form-control'}),
            'mid': forms.NumberInput(attrs={'class': 'form-control'}),
            'treble': forms.NumberInput(attrs={'class': 'form-control'}),
            'reverb': forms.NumberInput(attrs={'class': 'form-control'}),
            'audio_demo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
