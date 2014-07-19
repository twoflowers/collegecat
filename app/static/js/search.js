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
}