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