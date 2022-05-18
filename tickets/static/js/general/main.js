function sendMessage(personId, sendByEmail){

    // Function to send message to a person
    // message <string> : the message to be sent
    // subject <string> : the subject of the message to be sent
    // person_id <int> : the id of the person who is going to receive the message 
    // email <bool> : when true the way to send a message will be with an email
    // phone <bool> : when true the way to send a message will be with a text message (twilio)

    btnSendEmail = $('#send-email-btn')
    btnSendSms = $('#send-sms-btn')

    btnSendEmail.attr("disabled", true)
    btnSendEmail.text('Sending...')

    btnSendSms.attr("disabled", true)
    btnSendSms.text('Sending...')
    
    jsonData = {

        'message': $('#message-text').val(),
        'subject': $('#message-subject').val(),
        'person_id': personId,
        'send_by_email': sendByEmail,
    }

    $.ajax({
        type: 'POST',
        url: '/communications/send-message/',
        data: jsonData,
        headers: {"Authorization": "Token 62a39d368f74e6f7cbc5e4926c781f61a087517a"},
        success: function (response) {

            alert('Message sent successfully');

            afterSendMessage(success=true)

        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
            console.log(response);

            afterSendMessage(success=false)

        }
    });

}

function afterSendMessage(success){
    btnSendEmail.attr("disabled", false)
    btnSendEmail.text('Send message by email')

    btnSendSms.attr("disabled", false)
    btnSendSms.text('Send message by phone')

    if (success == true) {
        $('#message-text').val('');
        $('#message-subject').val('');

        $('#close-modal').click();

    }



}