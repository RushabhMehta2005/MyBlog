$(document).ready(function() {
    var csrfToken = $('#csrf-form input[name=csrfmiddlewaretoken]').val();

    $('.like-button').click(function() {
        var blogId = $(this).data('id');
        var likeCount = '#like-count-' + blogId;
        console.log('Blog ID:', blogId);
        $.ajax({
            url: "/blog/like/" + blogId + "/",
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(response) {
                console.log('Response:', response);
                $(likeCount).text(response.likes);
            },
            error: function(xhr, status, error) {
                console.error("Error: ", error, status);
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    // Display the error message in the message container
                    $('#message-container').text(xhr.responseJSON.error).show();
                }
            },         
        });
    });

    $('.comment-form').submit(function(event) {
        event.preventDefault();
        var blogId = $(this).data('id');
        var content = $(this).find('textarea[name="content"]').val();
        var commentsDiv = '#comments-' + blogId;

        $.ajax({
            url: "/blog/comment/" + blogId + "/",
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'content': content
            },
            success: function(response) {
                console.log('Response:', response);
                $(commentsDiv).append('<p><strong>' + response.user + ':</strong> ' + response.content + ' (' + response.created_at + ')</p>');
                $(this).find('textarea[name="content"]').val(''); // Clear the textarea
            }.bind(this),
            error: function(xhr, status, error) {
                console.error("Error: ", error, status);
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert(xhr.responseJSON.error);
                }
            }
        });
    });
});
