from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PresetForm, SignUpForm
from .models import Band, Preset


def search_presets(presets, q):
    # match song, amp model, band name or author username
    if q:
        presets = presets.filter(
            Q(song_name__icontains=q) |
            Q(amp_model__icontains=q) |
            Q(band__name__icontains=q) |
            Q(author__username__icontains=q)
        )
    return presets


def preset_list(request):
    band_id = request.GET.get('band')

    # remember the last chosen band in the session
    if band_id is not None:
        if band_id:
            request.session['last_band_id'] = band_id
        else:
            request.session.pop('last_band_id', None)
    else:
        band_id = request.session.get('last_band_id')

    q = request.GET.get('q', '').strip()

    presets = Preset.objects.all()
    if band_id:
        presets = presets.filter(band_id=band_id)
    presets = search_presets(presets, q)

    context = {
        'presets': presets,
        'bands': Band.objects.all(),
        'selected_band_id': str(band_id) if band_id else '',
        'search_query': q,
    }
    return render(request, 'presets/preset_list.html', context)


def presets_json(request):
    band_id = request.GET.get('band', '')
    if band_id:
        request.session['last_band_id'] = band_id
    else:
        request.session.pop('last_band_id', None)

    q = request.GET.get('q', '').strip()

    presets = Preset.objects.all()
    if band_id:
        presets = presets.filter(band_id=band_id)
    presets = search_presets(presets, q)

    data = []
    for p in presets:
        data.append({
            'id': p.id,
            'song_name': p.song_name,
            'amp_model': p.amp_model,
            'band': p.band.name,
            'author': p.author.username,
            'gain': p.gain,
            'bass': p.bass,
            'mid': p.mid,
            'treble': p.treble,
            'reverb': p.reverb,
            'url': p.get_absolute_url(),
        })
    return JsonResponse({'presets': data})


def preset_detail(request, pk):
    preset = get_object_or_404(Preset, pk=pk)
    return render(request, 'presets/preset_detail.html', {'preset': preset})


@login_required
def preset_create(request):
    if request.method == 'POST':
        form = PresetForm(request.POST, request.FILES)
        if form.is_valid():
            preset = form.save(commit=False)
            preset.author = request.user
            preset.save()
            return redirect(preset)
    else:
        form = PresetForm()
    return render(request, 'presets/preset_form.html', {'form': form})


@login_required
def preset_edit(request, pk):
    preset = get_object_or_404(Preset, pk=pk)
    if preset.author != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = PresetForm(request.POST, request.FILES, instance=preset)
        if form.is_valid():
            form.save()
            return redirect(preset)
    else:
        form = PresetForm(instance=preset)
    return render(request, 'presets/preset_form.html', {'form': form})


@login_required
def preset_delete(request, pk):
    preset = get_object_or_404(Preset, pk=pk)
    if preset.author != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        preset.delete()
        return redirect('preset_list')
    return render(request, 'presets/preset_confirm_delete.html', {'preset': preset})


def preset_download(request, pk):
    preset = get_object_or_404(Preset, pk=pk)
    content = 'ToneVault preset: ' + preset.song_name + '\n'
    content += 'Band: ' + preset.band.name + '\n'
    content += 'Amp model: ' + preset.amp_model + '\n'
    content += '-' * 30 + '\n'
    content += 'Gain:   ' + str(preset.gain) + '\n'
    content += 'Bass:   ' + str(preset.bass) + '\n'
    content += 'Mid:    ' + str(preset.mid) + '\n'
    content += 'Treble: ' + str(preset.treble) + '\n'
    content += 'Reverb: ' + str(preset.reverb) + '\n'
    content += '-' * 30 + '\n'
    content += 'Author: ' + preset.author.username + '\n'

    response = HttpResponse(content, content_type='text/plain')
    filename = f'tonevault_preset_{preset.pk}.txt'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('preset_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})
