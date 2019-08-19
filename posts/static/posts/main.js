var jqXHR;

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

    $(document).on('submit', '.new-post-form-ajax', function(e)  {
        e.preventDefault();
        var $form = $(this);
        var $formData = $form.serialize();
        var $formMethod = $form.attr('method');
        $.ajax({
            type: $formMethod,
            url: '/ajax/post/new/',
            data: $formData,
            success: function(data) {
                if (data.form_is_valid) {
                    console.log('Post was successfully added.');
                    if ($('.empty-posts').length) {
                        $('.empty-posts').remove();
                        // $('.empty-posts').addClass('hidden');
                    }
                    $('.posts').prepend(data.post).hide().fadeIn();
                    $('#view-comments-btn-' + data.pk ).html(data.comments_count);
                    $('#post-' + data.pk).css('background-color', '#FFFFFF');
                    $form[0].reset();
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

    $(document).on('submit', '.new-comment-form-ajax', function(e) {
        e.preventDefault();
        $form = $(this);
        var $formData = $form.serialize();
        var $post_id = $form.data('newcomment-form-id');
        var $postComments = $('[data-viewcomments-id=' + $post_id + ']');
        var $formMethod = $form.attr('method');
        $.ajax({
            type: $formMethod,
            url: '/ajax/comment/new/',
            data: $formData + "&pk=" + $post_id,
            success: function(data) {
                if (data.form_is_valid) {
                    console.log('Comment was successfully added.');
                    $postComments.removeClass('hidden');
                    $form[0].reset();
                    $form.addClass('hidden');
                    $empty_comments = $('[data-empty-post-comments-id=' + data.post_id + ']');
                    if ($empty_comments.length) {
                        $empty_comments.remove();
                    }
                    $('[data-post-comments-id=' + $post_id + ']').prepend(data.comment).hide().fadeIn();
                    $('#view-comments-btn-' + $post_id).html(data.comments_count);

                    var $comment = $('.list-group-item.comment-' + data.pk);
                    $comment.css('background-color', '#FFFFFF ');
                    window.setTimeout(function() {
                        $comment.css('background-color', '#C1CCD7');
                    }, 3000);
                }
                else {
                    console.log('Comment Creation Failed.');
                }
            }
        });
        return false;
    });


    $(document).on('submit', '.comment-delete-form', function(e) {
        e.preventDefault()
        var $comment_id = $(this).data('comment-delete-form');
        var $comment = $("#comment-" + $comment_id);
        $.ajax({
            type: "POST",
            url: '/ajax/comment/delete/',
            data: {
                'pk': $comment_id
            },
            success: function(data) {
                console.log('Comment deletion was successfull');
                $('#confirmDeleteComment' + $comment_id).modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();

                $('#view-comments-btn-' + data.post_id).html(data.comments_count);
                $comment.slideUp("normal", function() {
                    $(this).remove();
                });

                if (data.empty_comments) {
                    $('[data-viewcomments-id=' + data.post_id + ']').html(data.empty_comments)
                }
            }
        });
        return false;
    });

    $(document).on('click', '.edit-post-btn', function(e) {
        e.preventDefault()
        var $post_id = $(this).data('edit-post-btn');
        var $post = $("#post-" + $post_id);
        $.ajax({
            type: "GET",
            url: '/ajax/post/' + $post_id + '/edit/',
            success: function(data) {
                $post.find($('.post-editable-content')).html(data.edit_post_form);
                $post.css('background-color', '#FFFFFF');
            }
        });
    });

    $(document).on('click', '.edit-comment-btn', function(e) {
        e.preventDefault()
        var $comment_id = $(this).data('edit-comment-btn');
        var $comment = $("#comment-" + $comment_id);
        $.ajax({
            type: "GET",
            url: '/ajax/comment/' + $comment_id + '/edit/',
            success: function(data) {
                $comment.find($('.comment-editable-content')).html(data.edit_comment_form);
                $comment.css('background-color', '#FFFFFF');
            }
        });
    });

    $(document).on('submit', '.edit-post-form-ajax', function(e) {
        e.preventDefault();
        var $formData = $(this).serialize();
        var $post_id = $('.edit-post-confirm').data('edit-post-confirm');
        var $post = $("#post-" + $post_id);
        jqXHR = $.ajax({
            type: "POST",
            url: '/ajax/post/' + $post_id + '/edit/',
            data: $formData,
            success: function(data) {
                if (data.form_is_valid) {
                    console.log('Post was successfully editted');
                    $post.find($('.post-editable-content')).html(data.post);
                    $post.css('background-color', '#FFFFFF');
                    window.setTimeout(function() {
                        $post.css('background-color', '#E3E8ED');
                    }, 3000);
                }
                else {
                    console.log('Post Edit Failed');
                }
            }
        });
        return false;
    });

    $(document).on('submit', '.edit-comment-form-ajax', function(e) {
        e.preventDefault();
        var $formData = $(this).serialize();
        var $comment_id = $('.edit-comment-confirm').data('edit-comment-confirm');
        var $comment = $("#comment-" + $comment_id);
        jqXHR = $.ajax({
            type: "POST",
            url: '/ajax/comment/' + $comment_id + '/edit/',
            data: $formData,
            success: function(data) {
                if (data.form_is_valid) {
                    console.log('Comment was successfully editted');
                    $comment.find($('.comment-editable-content')).html(data.comment);
                    $comment.css('background-color', '#FFFFFF ');
                    window.setTimeout(function() {
                        $comment.css('background-color', '#C1CCD7');
                    }, 3000);
                }
                else {
                    alert('Comment Edit Failed');
                }
            }
        });
        return false;
    });


    $(document).on('click', '.cancel-edit-post', function(e) {
        e.preventDefault()
        var $post_id = $(this).data('cancel-edit-post');
        var $post = $("#post-" + $post_id);
        $.ajax({
            type: "GET",
            url: '/ajax/post/' + $post_id + '/edit/cancel/',
            success: function(data) {
                $post.find($('.post-editable-content')).html(data.post);
                $post.css('background-color', '#E3E8ED');
            }
        });
    });

    $(document).on('click', '.cancel-edit-comment', function(e) {
        e.preventDefault()
        var $comment_id = $(this).data('cancel-edit-comment');
        var $comment = $("#comment-" + $comment_id);
        $.ajax({
            type: "GET",
            url: '/ajax/comment/' + $comment_id + '/edit/cancel/',
            success: function(data) {
                $comment.find($('.comment-editable-content')).html(data.comment);
                $comment.css('background-color', '#C1CCD7');

            }
        });
    });

    $(document).on('submit', '.post-delete-form', function(e) {
        e.preventDefault()
        var $post_id = $(this).data('post-delete-form');
        var $post = $("#post-" + $post_id);
        $.ajax({
            type: "POST",
            url: '/ajax/post/delete/',
            data: {
                'pk': $post_id
            },
            success: function(data) {
                console.log('Post deletion was successfull');
                if (data.redirect) {
                    window.location.href = data.redirect
                }
                else {
                    $('.modal-backdrop').remove();
                    $('#confirmDeletePost' + $post_id).modal('hide');
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();

                    $post.slideUp("normal", function() {
                        $(this).remove();
                    });

                    if ($('.posts').find('.post').length === 1) {
                        $('.posts').html('<h3 class="content-section text-center py-4 empty-posts"><strong>This page has no posts.</strong></h3>');
                    }
                }
            }
        });
        return false;
    });



});
