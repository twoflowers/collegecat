$('#radius_0').on('click',  function() { change_radius(0); });
$('#radius_5').on('click',  function() { change_radius(5); });
$('#radius_10').on('click', function() { change_radius(10); });
$('#radius_25').on('click', function() { change_radius(25); });
$('#search_button').on('click', function() { search($('#search').val(), $('#location').val(), $('#radius').val()); })

function change_radius(radius) {
    $('#radius').val(radius);
    if (radius)
        $('#radius_dropdown').text('Within ' + radius + ' miles ');
    else
        $('#radius_dropdown').text('Unlimited ');
}

function search(subject, location, radius) {
    if (!subject || !location) {
        // TODO: error message
        return;
    }

    console.log('Search subject: ' + subject);
    console.log('Search location: ' + location);
    console.log('Search radius: ' + radius);

    // TODO: ajax search
    populate_search_results();
}

function populate_search_results() {
    // TODO: populate search results
    var data = [
        {'name': 'John Q. Public1'},
        {'name': 'John Q. Public2'},
    ];
    results_container = $('#search_results');
    var results_html = '';
    for (var index in data) {
        console.log(data[index]);
        results_html += tmpl('results_template', data[index]);
    }
    results_container.html(results_html);
}

function get_location() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(show_position);
    }
}

function show_position(position) {
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[1]) {
                set_location(results[1].formatted_address);
            }
        }
    });
}

function set_location(location) {
    $('#location').val(location);
}

window.onload = function () { get_location() };