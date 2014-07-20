$('#logout_button').on('click', function() {
    delete(profile);
    $('#profile_buttons').hide();
    $('#anonymous_buttons').show();
    $('#greet_user').hide();
    $('#profile_user').hide();
    $('#greet_anonymous').show();
    $('#why').show();
});

$('#login_button').on('click', function () {
    var login_button = $(this);
    login_button.button('loading');
    $.ajax({
        url: "/api/login/" + $('#email').val(),
    })
    .done(function(data) {
        login(data, login_button);
    })
    .error(function () {
        login_button.button('reset')
    });
});

function login(data, login_button) {
    $.ajax({
        url: "/api/profile/" + data['id'],
    })
    .done(function(data) {
        profile = data['data'];
        console.log('Profile', profile);

        $('#profile_buttons').show();
        $('#anonymous_buttons').hide();
        $('#login_modal').modal('hide');
        $('#greet_anonymous').hide();
        $('#search_results').hide();
        $('#why').hide();

        greet_container = $('#greet_user');
        var greet_html = tmpl('greet_user_template', profile['user']);
        greet_container.html(greet_html).show();

        profile_container = $('#profile_user');
        var profile_html = tmpl('profile_user_template', profile);
        profile_container.html(profile_html).show();

        $('.delete_appt').on('click', function() {
            delete_appt($(this));
        });
        $('.invoice_appt').on('click', function() {
            invoice_appt($(this));
        });
    })
    .always(function () {
        if (typeof login_button != 'undefined') {
            login_button.button('reset');
        }
    });
}

function delete_appt(element) {
    var id = element.data('appointment-id');
    element.button('loading');

    $.ajax({
        url: "/api/delete_appointment/" + id,
    })
    .done(function(data) {
        login(profile['user']);
    })
    .always(function () {
        element.button('reset');
    });
}

function invoice_appt(element) {
    var id = element.data('appointment-id');
    element.button('loading');

    $.ajax({
        url: "/api/create_invoice/" + id + "/" + parseInt(Math.floor((Math.random() * 9900) + 100), 10),
    })
    .done(function(data) {
        login(profile['user']);
    })
    .always(function () {
        element.button('reset');
    });
}

$('#profile_button').on('click', function () {
    if (profile) {
        $('#greet_user').show();
    } else {
        $('#greet_anonymous').show();
        $('#why').show();
    }

    $('#search_results').hide();
    $('#profile_user').show();
});

function send_message(element) {
    var id = element.data('contact-id');
    element.button('loading');

    var subject = '';

    $("#subject_" + id + " option:selected").each(function() {
        subject += $(this).text() + " ";
    });

    $.ajax({
        url: "/api/create_appointment/" + id,
        type: 'POST',
        data: {
            'user_id': profile['user']['id'],
            'subject': subject,
            'message': $('#contact_message_' + id).val()
        }
    })
    .done(function(data) {
        $('#contact_' + id).modal('hide');
        login(profile['user']);
    })
    .always(function () {
        element.button('reset')
    });
}

$('#profile_button').on('click', function () {
    if (profile) {
        $('#greet_user').show();
    } else {
        $('#greet_anonymous').show();
        $('#why').show();
    }

    $('#search_results').hide();
    $('#profile_user').show();
});

var profile;