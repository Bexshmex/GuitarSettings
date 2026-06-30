var select = document.getElementById("band-filter");
var listEl = document.getElementById("preset-list");

function cardHtml(p) {
    return (
        '<div class="col">' +
        '<div class="card h-100 shadow-sm">' +
        '<div class="card-body">' +
        '<h5 class="card-title mb-1">' + p.song_name + "</h5>" +
        '<h6 class="card-subtitle text-muted mb-2">' + p.band + "</h6>" +
        '<p class="card-text mb-2"><span class="badge bg-secondary">' +
        p.amp_model + "</span></p>" +
        '<p class="card-text small text-muted mb-3">' +
        "G " + p.gain + " &middot; B " + p.bass +
        " &middot; M " + p.mid + " &middot; T " + p.treble +
        " &middot; Rev " + p.reverb + "</p>" +
        '<a href="' + p.url + '" class="btn btn-sm btn-primary">View</a>' +
        "</div>" +
        '<div class="card-footer text-muted small">by ' + p.author + "</div>" +
        "</div></div>"
    );
}

function render(presets) {
    if (!presets.length) {
        listEl.innerHTML = '<p class="text-muted" id="empty-msg">No presets yet.</p>';
        return;
    }
    var html = "";
    for (var i = 0; i < presets.length; i++) {
        html += cardHtml(presets[i]);
    }
    listEl.innerHTML = html;
}

function loadPresets(bandId) {
    var url = window.PRESETS_JSON_URL + "?band=" + encodeURIComponent(bandId);
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(function (resp) {
            return resp.json();
        })
        .then(function (data) {
            render(data.presets || []);
        });
}

if (select && listEl && window.PRESETS_JSON_URL) {
    select.addEventListener("change", function () {
        loadPresets(select.value);
    });
}
