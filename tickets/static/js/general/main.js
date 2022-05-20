function sendMessage(personId = null, sendToTenant, sendByEmail) {
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

  if (personId === null) {
    personId = $("#input-tenant-id").val();
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

  if (sendToTenant == true) {
    jsonData.tenant_id = personId;
  } else {
    jsonData.supplier_id = personId;
  }

  $.ajax({
    type: "POST",
    url: "/communications/send-message/",
    data: jsonData,
    headers: {
      Authorization: "Token 8183c7dee6e75605837af987065b8baf0b36c3a1",
    },
    success: function (response) {
      Toastify({
        text: "Message sent successfully ✅",

        duration: 3000,
        style: {
          background: "green",
        },
      }).showToast();

      afterSendMessage((success = true));
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

      afterSendMessage((success = false));
    },
  });
}

function afterSendMessage(success) {
  btnSendEmail.attr("disabled", false);
  btnSendEmail.text("Send message by email");

  btnSendSms.attr("disabled", false);
  btnSendSms.text("Send message by phone");

  if (success == true) {
    $("#message-text").val("");
    $("#message-subject").val("");

    $("#close-modal").click();
  }
}

function setTenantInModalTabId(tenant_id) {
  $("#input-tenant-id").val(tenant_id);
}
