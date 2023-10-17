// function to enable darkmode
function enableDarkMode() {
    const body = document.querySelector('body');
    body.classList.add('dark-mode');
}

// function to disable darkmode
function disableDarkMode() {
    const body = document.querySelector('body');
    body.classList.remove('dark-mode');
}

// Event-Handler for dark mode button
const darkModeToggle = document.querySelector('#dark-mode-toggle');
darkModeToggle.addEventListener('click', function () {
    if (document.body.classList.contains('dark-mode')) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
});

var selectedCar = ""; // Variable, um das ausgewählte Auto zu speichern

// Event-Handler for initials
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
// Event-Handler for initials select
$('#initials_select').change(function () {
    var initials = $(this).val();
    if (initials) {
        loadCars(initials);  // Lade die Autos basierend auf den ausgewählten Initialen
        displayTrack(null);  // Zeige keinen Track an, wenn Initialen ausgewählt werden
    }
});

// Funktion zum Laden der Autos basierend auf den ausgewählten Initialen
function loadCars(initials) {
    $.ajax({
        url: '/get_cars/' + initials,
        method: 'GET',
        success: function (data) {
            var carsSelect = $('#cars_select');
            carsSelect.empty();
            carsSelect.append($('<option>').val('').text('Wählen Sie ein Auto'));
            $.each(data, function (index, car) {
                carsSelect.append($('<option>').val(car).text(car));
            });
        }
    });
}


// Event-Handler for cars select
$('#cars_select').change(function () {
    selectedCar = $(this).val();
});

// function for displaying filtered track on map
function displayFilteredTrack() {
    var initials = $('#initials_select').val();
    var startDate = $('#start-date').val();
    var endDate = $('#end-date').val();

    if (initials && startDate && endDate) {
        // Check if a car is selected, if not, display an error message
        if (!selectedCar) {
            alert('Bitte wählen Sie ein Auto aus.');
            return;
        }

        // Display filtered track on the map
        $.ajax({
            url: '/display_track/' + initials + '/' + selectedCar + '/' + startDate + '/' + endDate,
            method: 'GET',
            success: function (mapHtml) {
                $('.map-container').html(mapHtml);
            }
        });
    } else {
        // Handle error, e.g., show a message to the user
        alert('Bitte wählen Sie Initialen und geben Sie Start-/Enddaten an.');
    }
}

// Event-Handler for the "Anwenden" button
$('#apply-filters').click(function () {
    displayFilteredTrack();
});

// Event-Handler für den Reset-Button
$('#reset-filters').click(function () {
    // Leere alle Dropdown-Menüs
    $('#initials_select, #cars_select').val('');
    $('#start-date, #end-date').val('');

    // Lade die Initialen neu
    loadInitials();

    // Setze die Karte auf ihre Standardposition zurück
    var defaultLatLng = [51.1657, 10.4515];
    var defaultZoom = 6;

    // Aktualisiere die Karte über die Flask-Route
    $.ajax({
        url: '/reset_map',
        method: 'GET',
        success: function (mapHtml) {
            $('.map-container').html(mapHtml);

            // Zentriere und setze den Zoom der Karte zurück
            var map = L.map('map').setView(defaultLatLng, defaultZoom);
        }
    });
});


// load initials on page startup
loadInitials();
