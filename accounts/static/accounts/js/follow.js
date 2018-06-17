$('.follow-button').click(function() {
    $.get($(this).data('url'), function(response) {
        $('.message-section').text(response.message).show();
    });
});