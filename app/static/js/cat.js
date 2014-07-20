$('#logout_button').on('click', function() {
    delete(profile);
    $('#profile_buttons').hide();
    $('#anonymous_buttons').show();
    $('#greet_user').hide();
    $('#greet_anonymous').show();
});

$('#login_button').on('click', function () {
    var login_button = $(this);
    login_button.button('loading');
    $.ajax({
        url: "/api/login/" + $('#email').val(),
    })
    .done(function(data) {
        profile = data;
        $('#profile_buttons').show();
        $('#anonymous_buttons').hide();
        $('#login_modal').modal('hide');
        $('#greet_anonymous').hide();

        greet_container = $('#greet_user');
        var greet_html = tmpl('greet_user_template', profile);
        greet_container.html(greet_html).show();
    }).always(function () {
        login_button.button('reset')
    });
});

var profile;