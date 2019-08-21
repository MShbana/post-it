$(function() {
    $("#id_username").on('input', function() {
        var $id_username = $(this);
        var $username = $(this).val();

        $.ajax({
            url: '/ajax/validate_username/',
            data: {
                'username': $username
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
        var $email = $(this).val();

        $.ajax({
            url: '/ajax/validate_email/',
            data: {
                'email': $email
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

    $(document).on('click', '.following-btn', function(e) {
        e.preventDefault();

        var $follow_button = $(this);
        var $slug = $(this).data('profile-slug');

        $follow_button.attr('disabled', true);

        $.ajax({
            type: 'POST',
            url: '/account/ajax/follow/',
            data: {
                'slug': $slug,
            },
            dataType: 'json',
            success: function(data) {
                if (data.is_following) {
                    $follow_button.text('Unfollow');
                    $follow_button.removeClass('btn-success');
                    $follow_button.addClass('btn-danger');
                } else {
                    $follow_button.text('Follow')
                    $follow_button.removeClass('btn-danger')
                    $follow_button.addClass('btn-success');
                }
            },
            complete: function() {
                $follow_button.attr('disabled', false);
            }
        });
        return false;
    });
});
