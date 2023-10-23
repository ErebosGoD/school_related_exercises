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

var selectedCar = "";

// Event-Handler for initials
function loadInitials() {
    $.ajax({
        url: '/get_initials',
        method: 'GET',
        success: function (data) {
            var initialsSelect = $('#initials_select');
            initialsSelect.empty();
            initialsSelect.append($('<option>').val('').text('Choose Initials'));
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
        loadCars(initials);  // load cars based on selected initials
        displayTrack(null);  // don't display track just yet, even if initials are selected
    }
});

// Function for loading cars based on selected initials
function loadCars(initials) {
    $.ajax({
        url: '/get_cars/' + initials,
        method: 'GET',
        success: function (data) {
            var carsSelect = $('#cars_select');
            carsSelect.empty();
            carsSelect.append($('<option>').val('').text('Choose a car'));
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
            alert('Please choose a car');
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
        alert('Please choose initials and enter start-/enddate');
    }
}

// Event-Handler for the "Anwenden" button
$('#apply-filters').click(function () {
    displayFilteredTrack();
});

// Event-Handler for the Reset-Button
$('#reset-filters').click(function () {
    // Clear all Dropdown-Menus
    $('#initials_select, #cars_select').val('');
    $('#start-date, #end-date').val('');

    // Load initials again
    loadInitials();

    // Update map through
    $.ajax({
        url: '/reset_map',
        method: 'GET',
        success: function (mapHtml) {
            $('.map-container').html(mapHtml);
        }
    });
});


// load initials on page startup
loadInitials();
