$(function() {
    $('.following-btn').on('click', function(e) {
        e.preventDefault();

        var $follow_button = $(this);
        var $account_wrapper = $(this).closest('.list-group-item');
        var $slug = $(this).data('profile-slug');

        $.ajax({
            type: 'POST',
            url: '/account/ajax/follow/',
            data: {
                'slug': $slug,
            },
            dataType: 'json',
            success: function(data) {
                $follow_button.text('Unfollow');
                $follow_button.removeClass('btn-success');
                $follow_button.addClass('btn-danger');
                $account_wrapper.fadeTo(500, 0.4, function() {
                    $(this).slideUp();
                });
            }
        });
        return false;
    });


    $('.comment-delete').on("click",function(){
        $(window).scrollTop(0);
    });


    var $newPostForm = $('.new-post-form-ajax')

    $newPostForm.on('submit', function(e)  {
        $(this).submit(false);
        e.preventDefault();

        var $form = $(this);
        var $formData = $form.serialize();
        var $URL = $form.attr('data-url') || window.location.href;
        var $formMethod = $form.attr('method');

        $.ajax({
            type: $formMethod,
            url: $URL,
            data: $formData,
            success: function(data) {
                if (data.form_is_valid) {
                    console.log('Post was successfully added.');
                    $('.posts').html(data.posts);
                    var $postID = $('#post-' + data.pk);
                    $form[0].reset();
                    var $successAlert = $('div.new-post-success');
                    $successAlert.show();
                    $postID.css('background-color', '#FFFFFF');
                    setTimeout(function(){
                        $postID.css('background-color', '#C1CCD7');
                        $successAlert.fadeTo(500, 0).slideUp(500, function(){
                            $(this).remove();
                        });
                    }, 3000)
                }
                else {
                    console.log('Post Creation Failed.');
                }
            }
        });
        return false;
    });


    window.setTimeout(function() {
        $(".alert-message").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove();
        });
    }, 3000);
});
