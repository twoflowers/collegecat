var gps = {};

$('#radius_0').on('click',   function() { change_radius(0); });
$('#radius_25').on('click',  function() { change_radius(25); });
$('#radius_50').on('click',  function() { change_radius(50); });
$('#radius_100').on('click', function() { change_radius(100); });
$('#search_button').on('click', function() { search($('#search').val(), $('#location').val(), $('#radius').val()); });

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

    populate_search_results();
}

function populate_search_results() {
    var data = [];
    $.ajax({
        url: "/api/search/?query=" + $('#search').val() + "&lat=" + gps.lat + "&lon=" + gps.long + "&radius=" + $('#radius').val()
    })
        .done(function (results) {
            data = results.data;
            console.log("Found results");
            console.log(data);

            if (data) {
                $('#why').hide();
                $('#profile_user').hide();
                $('#search_results').show();
            }

            results_container = $('#search_results');
            var results_html = '';
            var ids = [];
            for (var index in data) {
                console.log(data[index]);
                console.log(index);
                results_html += tmpl('results_template', data[index]);
                ids.push(data[index]['id']);
            }
            results_container.html(results_html);
            for (var index in ids) {
                $('#subjects_' + ids[index]).select2({});
            }

            $('.request_appt_button').on('click', function () {
                send_message($(this));
            });
        })
        .error(function () {
            console.log("Error loading search results");
        });
//    var data = [
//        {'id': 346, 'name': 'Tom Martin',    'rating': 3, 'price': [12, 10, 1], 'subjects': ['math', 'programming', 'sheep'], 'availability': 'Anytime', 'bio': 'yo', 'latitude': '38.9237738', 'longitude': '-94.7306424'},
//        {'id': 12346, 'name': 'Stan Antov',    'rating': 5, 'price': [100, 5, 120], 'subjects': ['design', 'programming', 'goats'], 'availability': 'Anytime', 'bio': 'yo', 'latitude': '38.9237738', 'longitude': '-94.7306424'},
//        {'id': 12347, 'name': 'Marc Streeter', 'rating': 4, 'price': [150], 'subjects': ['chupacabras'], 'availability': 'Anytime', 'bio': 'yo', 'latitude': '38.9237738', 'longitude': '-94.7306424'},
//    ];


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
                gps.lat = position.coords.latitude;
                gps.long = position.coords.longitude;
            }
        }
    });
}

function set_location(location) {
    $('#location').val(location);
}

function set_search(search) {
    $('#search').val(search);
}

String.prototype.capitalize = function() {
    return this.replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
};

$.get('/api/subjects', function(data) {
    var subjects = [];
    for (var index in data) {
        subjects.push(data[index]['name']);
    }

    $("#search").typeahead({source: subjects});
},'json');

window.onload = function () { get_location() };
//window.onload = function () { set_location('Overland Park, KS'); set_search(''); };
