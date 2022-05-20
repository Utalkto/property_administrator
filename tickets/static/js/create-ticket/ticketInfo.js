function makeComment(ticketId) {


    comment = $('#comment-input')

    if ( comment.val().trim() == ''){
        alert('You cannot leave comment empty');
        return
    }
    
    jsonData = {
        'comment' : comment.val(),
    }


    $.ajax({
        type: 'POST',
        url: `/tickets/ticket-comment/${ticketId}`,
        data: jsonData,
        headers: {"Authorization": "Token d0610c6848b24e10e7a41b17acd3cf485213da8c"},
        success: function (response) {

            alert('Message sent successfully');

            afterCommentMade(response);
            comment.val('')

        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
            console.log(response);

        }
    });
}


function afterCommentMade(data) {

    commentsTitle = $('#ticket-comments-title')

    if (commentsTitle === null) {

        $('#comments-section').append(
            `<h4 id="ticket-comments-title">Ticket Comments</h4>`
        )

    }


    $('#comments-made').prepend(

        `<hr>

        <p><strong>Created at : Just few seconds ago</strong></p>
        <p><strong>Made by : ${data.made_by}</strong></p>

      
        <p>${data.comment.comment}</p>

        <hr>`

    )

}