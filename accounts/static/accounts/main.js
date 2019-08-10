$("#id_username").on('input', function() {
    var $id_username = $(this);
    var $id_username_val = $(this).val();

    $.ajax({
        url: '/ajax/validate_username',
        data: {
            'username': $id_username_val
        },
        dataType: 'json',
        success: function(data) {
            if (data.is_taken) {
                $id_username.css('color', 'red');
                $id_username.css('color', 'red');
            } else {
                $id_username.css('color', '#CED4DA');
                $id_username.css('color', 'black');
            }
        }
    });
});


$("#id_email").on('input', function() {
    var $id_email = $(this);
    var $id_email_val = $(this).val();

    $.ajax({
        url: '/ajax/validate_email',
        data: {
            'email': $id_email_val
        },
        dataType: 'json',
        success: function(data) {
            if (data.is_taken) {
                $id_email.css('color', 'red');
                $id_email.css('color', 'red');
            } else {
                $id_email.css('color', '#CED4DA');
                $id_email.css('color', 'black');
            }
        }
    });
});
