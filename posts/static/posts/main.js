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


    // $('.comment-delete').on("click",function(){
    //     $(window).scrollTop(0);
    // });


    $('.new-post-form-ajax').on('submit', function(e)  {
        $(this).submit(false);
        e.preventDefault();
        var $form = $(this);
        var $formData = $form.serialize();
        var $formMethod = $form.attr('method');
        $.ajax({
            type: $formMethod,
            url: '/ajax/new_post/',
            data: $formData,
            success: function(data) {
                if (data.form_is_valid) {
                    console.log('Post was successfully added.');
                    $('.posts').prepend(data.post);
                    $('#view-comments-btn-' + data.pk ).html(data.comments_count);
                    $('#post-' + data.pk).css('background-color', '#FFFFFF');
                    $form[0].reset();
                    $('div.new-post-success').show().delay(500).fadeOut(3000);
                    window.setTimeout(function() {
                        $('#post-' + data.pk).css('background-color', '#E3E8ED');
                    }, 3000);
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


    $(document).on('click', '.new-comment-btn', function(e) {
        var $post_id = $(this).data('newcomment-btn-id');
        var $commentForm = $('[data-newcomment-form-id=' + $post_id + ']');
        var $postComments = $('[data-viewcomments-id=' + $post_id + ']');
        $commentForm.toggleClass('hidden');
        if ($postComments.length > 0 ) {
            $postComments.addClass('hidden');
        }
    });


    $(document).on('click', '.view-comments-btn', function(e) {
        var $post_id = $(this).data('viewcomments-btn-id');
        var $postComments = $('[data-viewcomments-id=' + $post_id + ']');
        var $commentForm = $('[data-newcomment-form-id=' + $post_id + ']');
        $postComments.toggleClass('hidden');
        if ($commentForm.length > 0) {
            $commentForm.addClass('hidden');
        }
    });

    $(document).on('submit', '.new-comment-form', function(e) {
        e.preventDefault();
        $form = $(this);
        var $formData = $form.serialize();
        var $post_id = $form.data('newcomment-form-id');
        var $postComments = $('[data-viewcomments-id=' + $post_id + ']');
        var $formMethod = $form.attr('method');
        $.ajax({
            type: $formMethod,
            url: '/ajax/new_comment/',
            data: $formData + "&id=" + $post_id,
            success: function(data) {
                if (data.form_is_valid) {
                    $postComments.html(data.comments);
                    $('#view-comments-btn-' + $post_id).html(data.comments_count);
                    $postComments.removeClass('hidden');
                    $form[0].reset();
                    $form.addClass('hidden');
                    var $comment = $('.list-group-item.comment-' + data.pk);
                    $comment.css('background-color', '#FFFFFF ');
                    window.setTimeout(function() {
                        $comment.css('background-color', '#C1CCD7');
                    }, 3000);
                    console.log('Comment was successfully added.');
                }
                else {
                    console.log('Comment Creation Failed.');
                }
            }
        });
        return false;
    });
});