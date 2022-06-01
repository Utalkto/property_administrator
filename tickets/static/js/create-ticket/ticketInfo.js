let ticketId = $('#ticket-id').val();


function makeComment(ticketId) {
  comment = $("#comment-input");

  if (comment.val().trim() == "") {
    alert("You cannot leave comment empty");
    return;
  }

  jsonData = {
    comment: comment.val(),
  };

  $.ajax({
    type: "POST",
    url: `/tickets/ticket-comment/${ticketId}`,
    data: jsonData,
    headers: {
      Authorization: `Token ${$('#auth-token').val()}`,
    },
    success: function (response) {
      afterCommentMade(response);
      comment.val("");
    },
    error: function (response) {
      alert("An error has ocurred with your message, please try again.");
      console.log(response);
    },
  });
}


function afterCommentMade(data) {
  commentsTitle = $("#ticket-comments-title");

  if (commentsTitle === null) {
    $("#comments-section").append(
      `<h4 id="ticket-comments-title">Ticket Comments</h4>`
    );
  }

  $("#comments-made").prepend(
    `<hr>

        <p><strong>Created at : Just few seconds ago</strong></p>
        <p><strong>Made by : ${data.made_by}</strong></p>

      
        <p>${data.comment.comment}</p>

        <hr>`
  );
}


function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}


// button fuctions 

$("#close-ticket").click(() => {

  bootbox.confirm({
    title: "Close ticket",
    message:
      "Are you sure the problem has been solved?",
    buttons: {
      cancel: {
        label: '<i class="fa fa-times"></i> Cancel',
      },
      confirm: {
        label: '<i class="fa fa-check"></i> Close ticket',
      },
    },
    callback: function (result) {

      if (result===true) {

        $.ajax({
          type: "POST",
          url: `/tickets/close-ticket/${ticketId}`,
          headers: {
            Authorization: `Token ${$('#auth-token').val()}`,
          },
          success: function (response) {

            Toastify({
              text: "The ticket has beed closed",
              duration: 2000,
              style: {
                background: "green",
              },
            }).showToast();

           
          sleep(1000).then(() => {
            window.location.href = `http://154.12.240.122:8000/tickets/home/${$('#auth-token').val()}`;
          });

            

          },
          error: function (response) {
            alert("An error has ocurred with your message, please try again.");
            console.log(response);
          },
        })
      }
    },
  });

});


$('#problem-not-solved').click(() => {
  bootbox.confirm({
    title: "Problem is not solved",
    message:
    'Are you sure the problem is not solved? by pressing not solved it will return you to the coordinate visit secion',
    
    buttons: {
      cancel: {
        label: '<i class="fa fa-times"></i> Cancel',
      },
      confirm: {
        label: 'Not solved',
        className:'btn-danger',
      },
    },
    
    callback: function (result) {

      if (result===true) {

        $.ajax({
          type: "POST",
          url: `/tickets/return-to-coordinate-visit/${ticketId}`,
          headers: {
            Authorization: `Token ${$('#auth-token').val()}`,
          },
          success: function (response) {

            window.location.href = `http://154.12.240.122:8000/tickets/ticket-info/${$('#auth-token').val()}/${$('#ticket-id').val()}`;

          
          },
          error: function (response) {
            alert("An error has ocurred with your message, please try again.");
            console.log(response);
          },
        })
      }
    },
  });

})


$('#supplier-did-not-attend').click(() => {
  bootbox.confirm({
    title: "Confirm",
    message:
    'Please confirm that the contractor did not attend the appoinment',
    
    buttons: {
      cancel: {
        label: '<i class="fa fa-times"></i> Cancel',
      },
      confirm: {
        label: 'Confirm',
        className:'btn-danger',
      },
    },
    
    callback: function (result) {

      if (result===true) {

        $.ajax({
          type: "POST",
          data: {'no_attendance': true},
          url: `/tickets/return-to-coordinate-visit/${ticketId}`,
          headers: {
            Authorization: `Token ${$('#auth-token').val()}`,
          },
          success: function (response) {

            window.location.href = `http://154.12.240.122:8000/tickets/ticket-info/${$('#auth-token').val()}/${$('#ticket-id').val()}`;

          
          },
          error: function (response) {
            alert("An error has ocurred with your message, please try again.");
            console.log(response);
          },
        })
      }
    },
  });
});


$("#button-delete").click(() => {

  bootbox.confirm({
    title: "Delete ticket",
    message:
      "Are you sure you want to delete this ticket? eveything that is associeted with that will be deleted",
    buttons: {
      cancel: {
        label: '<i class="fa fa-times"></i> Cancel',
      },
      confirm: {
        label: '<i class="fa-solid fa-trash-can"></i> Delete',
        className:'btn-danger',
      },
    },
    callback: function (result) {

      if (result===true) {

        $.ajax({
          type: "DELETE",
          url: `/tickets/delete-ticket/${ticketId}`,
          headers: {
            Authorization: `Token ${$('#auth-token').val()}`,
          },
          success: function (response) {

            Toastify({
              text: "The ticket has beed deleted",
              duration: 2000,
              style: {
                background: "green",
              },
            }).showToast();

           
          sleep(1000).then(() => {
            window.location.href = `http://154.12.240.122:8000/tickets/home/${$('#auth-token').val()}`;
          });
          
          },
          error: function (response) {
            alert("An error has ocurred with your message, please try again.");
            console.log(response);
          },
        })

      }

    },
  });

});


$('#send-message-to-tenant').click(() => {
  $('#modal-send-message-div').removeAttr('hidden');
})

$("#close-modal").click(() => {
  $('#modal-send-message-div').attr('hidden', 'true');
});

$("#close-modal-2").click(() => {
  $('#modal-send-message-div').attr('hidden', 'true');
});



$('#mark-problem-as-completed').click(() => {
  $('#modal-div-2').removeAttr('hidden');
})


$('#set-payment-as-completed').click(() => {
  $('#modal-div-2').removeAttr('hidden');
})


$("#close-modal-3").click(() => {
  $('#modal-div-2').attr('hidden', 'true');
});

$("#close-modal-4").click(() => {
  $('#modal-div-2').attr('hidden', 'true');
});






