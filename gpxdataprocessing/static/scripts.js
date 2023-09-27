// Funktion zum Aktivieren des Dark Mode
function enableDarkMode() {
    const body = document.querySelector('body');
    body.classList.add('dark-mode');
}

// Funktion zum Deaktivieren des Dark Mode
function disableDarkMode() {
    const body = document.querySelector('body');
    body.classList.remove('dark-mode');
}

// Event-Handler für den Dark Mode-Button
const darkModeToggle = document.querySelector('#dark-mode-toggle');
darkModeToggle.addEventListener('click', function () {
    if (document.body.classList.contains('dark-mode')) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
});


// Funktion zum Laden der Initialen in das Dropdown-Menü
function loadInitials() {
    $.ajax({
        url: '/get_initials',
        method: 'GET',
        success: function (data) {
            var initialsSelect = $('#initials_select');
            initialsSelect.empty();
            initialsSelect.append($('<option>').val('').text('Wählen Sie Initialen'));
            $.each(data, function (index, initials) {
                initialsSelect.append($('<option>').val(initials).text(initials));
            });
        }
    });
}

// Funktion zum Laden der Tracks in das Dropdown-Menü
function loadTracks(initials) {
    $.ajax({
        url: '/get_tracks/' + initials,
        method: 'GET',
        success: function (data) {
            var tracksSelect = $('#tracks_select');
            tracksSelect.empty();
            tracksSelect.append($('<option>').val('').text('Wählen Sie einen Track'));
            $.each(data, function (index, trackId) {
                tracksSelect.append($('<option>').val(trackId).text('Track ' + trackId));
            });
        }
    });
}

// Funktion zum Anzeigen eines Tracks auf der Karte
function displayTrack(trackId) {
    if (trackId) {
        // Wegpunkte für den ausgewählten Track abrufen
        $.ajax({
            url: '/display_track/' + trackId,
            method: 'GET',
            success: function (mapHtml) {
                // Ersetzen Sie den Inhalt des "map-placeholder" <div> mit der Karte
                $('.map-container').html(mapHtml);
            }
        });
    } else {
        // Wenn kein Track ausgewählt ist, das "map-placeholder" <div> leeren
        $('#map-container').empty();
    }
}

// Event-Handler für die Auswahl einer Initialen
$('#initials_select').change(function () {
    var initials = $(this).val();
    if (initials) {
        loadTracks(initials);
        // Beim Ändern der Initialen die Karte leeren
        displayTrack(null);
    }
});

// Event-Handler für die Auswahl eines Tracks
$('#tracks_select').change(function () {
    var trackId = $(this).val();
    displayTrack(trackId);
});

// Initialen beim Laden der Seite laden
loadInitials();
