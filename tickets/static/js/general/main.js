const authToken =  $('#auth-token').val()


function sendMessage(personId = null, sendToTenant, sendByEmail, comFeed=false, supplierFeed=false) {
  // Function to send message to a person
  // message <string> : the message to be sent
  // subject <string> : the subject of the message to be sent
  // person_id <int> : the id of the person who is going to receive the message
  // email <bool> : when true the way to send a message will be with an email
  // phone <bool> : when true the way to send a message will be with a text message (twilio)

  message = $("#message-text");
  subject = $("#message-subject");

  if (message.val().trim() == "" || subject.val().trim() == "") {
    Toastify({
      text: "You cannot leave subject or message empty",

      duration: 2000,
      style: {
        background: "red",
        color: "white",
      },
    }).showToast();
    return;
  }

  if (personId == null) {
    personId = $("#person-id").val();
  }

  btnSendEmail = $("#send-email-btn");
  btnSendSms = $("#send-sms-btn");

  btnSendEmail.attr("disabled", true);
  btnSendEmail.text("Sending...");

  btnSendSms.attr("disabled", true);
  btnSendSms.text("Sending...");

  jsonData = {
    message: message.val(),
    subject: subject.val(),
    send_by_email: sendByEmail,
  };

  // checking if the message will be sent to a supplier or to a tenant

  if (sendToTenant == null) {
      t = $('#send-to-tenant').val();

      console.log(t)

      if (t == '1' || t == 1) {
        sendToTenant = 'True';
      } else {
        sendToTenant = false;
      }
  }

  if (sendToTenant == 'True') {
    jsonData.tenant_id = personId;
  } else {
    jsonData.supplier_id = personId;
  }

  console.log(jsonData)

  $.ajax({
    type: "POST",
    url: "/communications/send-message/",
    data: jsonData,
    headers: {
      Authorization: `Token ${$('#auth-token').val()}`,
    },
    success: function (response) {
      Toastify({
        text: "Message sent successfully ✅",

        duration: 3000,
        style: {
          background: "green",
        },
      }).showToast();

      
      afterSendMessage(success = true, comFeed = comFeed, supplierFeed = supplierFeed, response = response);
    },
    error: function (response) {
      Toastify({
        text: "An error has ocurred with your message, try again",
        duration: 2000,
        style: {
          background: "red",
        },
      }).showToast();

      

      console.log(response);
      afterSendMessage(success = false, comFeed = comFeed, supplierFeed = supplierFeed, response = response);
    },
  });
}


function afterSendMessage(success, comFeed, supplierFeed, response) {


  btnSendEmail.attr("disabled", false);
  btnSendEmail.text("Send message by email");

  btnSendSms.attr("disabled", false);
  btnSendSms.text("Send message by phone");

  if (success == true) {
    $("#message-text").val("");
    $("#message-subject").val("");

    $("#close-modal").click();
    $('#modal-send-message-div').attr('hidden', 'true');


    if ($(".modal-backdrop")[0] != null) {
      $(".modal-backdrop")[0].remove();
    }

    if (comFeed == true) {
      addMessageToSent(response);

      messagesSent = $('#messages-sent');
      messagesSent.text(parseInt(messagesSent.text()) + 1);
    }

    console.log()

    if (supplierFeed == true) {

      afterContactSupplier();

    }

  }
}


function setTenantInModalTabId(tenant_id, feed=false, sendToTenant=false) {
  $("#person-id").val(tenant_id);

  if (feed === 'True') {
    if (sendToTenant === 'True'){

      $('#send-to-tenant').val(1);

    } else {
      $('#send-to-tenant').val(0);

    }
  }

}


function setIdInModalTab(objectId) {
  $("#input-id").val(objectId);
}


function addMessageToSent(response) {

  $('#messages-section').prepend(`
  
  <div class="card">
    <div class="card-body">
        <div class="media media-reply">
            <div class="media-body">
                <div class="d-sm-flex justify-content-between mb-2">
                    <h5 class="mb-sm-0"> Made by: ${response.data.made_by}
                        <small class="text-muted ml-3">Via: ${ response.data.via }</small> 
                        <small class="text-muted ml-3">Sent at: A few seconds ago</small> 
                    </h5>
                
                </div>

                <br>
                <h6><strong> Subject: ${response.data.subject} </strong></h6>
                <br>
                
                <p>${response.data.message}</p>
            </div>
        </div>
    </div>
  </div>
  `)
}


function afterContactSupplier() {

  jsonData = {
    'supplier_id' : $('#person-id').val(),
    'ticket_id' : $('#ticket-id').val(),
    'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
  }

  $.ajax({
    type: "POST",
    url: "",
    data: jsonData,

    success: function (response) {

      window.location.href = `http://154.12.240.122:8000/tickets/ticket-info/${$('#auth-token').val()}/${$('#ticket-id').val()}`;
      
    },
    error: function (response) {
      Toastify({
        text: "An error has ocurred with your message, try again",
        duration: 2000,
        style: {
          background: "red",
        },
      }).showToast();

    },
  });

}



