function sendMessage(personId=null, sendToTenant, sendByEmail, ){

    // Function to send message to a person
    // message <string> : the message to be sent
    // subject <string> : the subject of the message to be sent
    // person_id <int> : the id of the person who is going to receive the message 
    // email <bool> : when true the way to send a message will be with an email
    // phone <bool> : when true the way to send a message will be with a text message (twilio)


    message = $('#message-text');
    subject = $('#message-subject');


    if ( message.val().trim() == ''  || subject.val().trim() == ''){
        alert('You cannot leave subject or message empty');
        return
    }


    if (personId === null){
        personId = $('#input-tenant-id').val();
    }

    btnSendEmail = $('#send-email-btn');
    btnSendSms = $('#send-sms-btn');

    btnSendEmail.attr("disabled", true);
    btnSendEmail.text('Sending...');

    btnSendSms.attr("disabled", true);
    btnSendSms.text('Sending...');

    jsonData = {

        'message': message.val(),
        'subject': subject.val(),
        'send_by_email': sendByEmail,
    }

    // checking if the message will be sent to a supplier or to a tenant 

    if (sendToTenant == true){
        jsonData.tenant_id = personId
    } 
    else {
        jsonData.supplier_id = personId
    }

    $.ajax({
        type: 'POST',
        url: '/communications/send-message/',
        data: jsonData,
        headers: {"Authorization": "Token 62a39d368f74e6f7cbc5e4926c781f61a087517a"},
        success: function (response) {

            alert('Message sent successfully');

            afterSendMessage(success=true);

        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
            console.log(response);

            afterSendMessage(success=false);

        }
    });

}

function afterSendMessage(success){
    btnSendEmail.attr("disabled", false);
    btnSendEmail.text('Send message by email');

    btnSendSms.attr("disabled", false);
    btnSendSms.text('Send message by phone');

    if (success == true) {
        $('#message-text').val('');
        $('#message-subject').val('');

        $('#close-modal').click();
    }
}


function setTenantInModalTabId(tenant_id){

    $('#input-tenant-id').val(tenant_id)

}