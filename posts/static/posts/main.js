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
                    $successAlert.show().delay(500).fadeOut(3000);

                    $postID.css('background-color', '#FFFFFF');
                    window.setTimeout(function() {
                        $postID.css('background-color', '#E3E8ED');
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


    var $newCommentBtn = $('.new-comment-btn');
    $newCommentBtn.on('click', function(e){
        var $btn = $(this);
        var $post_id = $(this).data('newcomment-btn-id');
        console.log($post_id);
        var $commentForm = $('[data-newcomment-form-id=' + $post_id + ']');
        var $postComments = $('[data-viewcomments-id=' + $post_id + ']');
        $commentForm.toggleClass('hidden');
        if ($postComments.length > 0 ) {
            $postComments.addClass('hidden');
        }
    });

    var $viewCommentsBtn = $('.view-comments-btn');
    $viewCommentsBtn.on('click', function() {
        var $btn = $(this);
        var $post_id = $(this).data('viewcomments-btn-id');
        var $postComments = $('[data-viewcomments-id=' + $post_id + ']');
        var $commentForm = $('[data-newcomment-form-id=' + $post_id + ']');
        $postComments.toggleClass('hidden');
        if ($commentForm.length > 0) {
            $commentForm.addClass('hidden');
        }
    });
});