<<<<<<< HEAD
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
      Authorization: "Token d0610c6848b24e10e7a41b17acd3cf485213da8c",
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


$("#close-ticket").click(() => {

  bootbox.confirm({
    title: "Confirm",
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

      $.ajax({
        type: "POST",
        url: `/tickets/close-ticket/${ticketId}`,
        headers: {
          Authorization: "Token d0610c6848b24e10e7a41b17acd3cf485213da8c",
        },
        success: function (response) {
          alert('the ticket has beed closed');
        },
        error: function (response) {
          alert("An error has ocurred with your message, please try again.");
          console.log(response);
        },

      })
    },
  });

});


=======
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
      Authorization: "Token d0610c6848b24e10e7a41b17acd3cf485213da8c",
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
            Authorization: "Token d0610c6848b24e10e7a41b17acd3cf485213da8c",
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
            window.location.href = `http://localhost:8000/tickets/`;
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
            Authorization: "Token d0610c6848b24e10e7a41b17acd3cf485213da8c",
          },
          success: function (response) {

            window.location.href = `http://localhost:8000/tickets/ticket-info/${ticketId}`;
          
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
            Authorization: "Token d0610c6848b24e10e7a41b17acd3cf485213da8c",
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
            window.location.href = `http://localhost:8000/tickets/`;
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





>>>>>>> 04a779ed2616815393f81adaed0bf232b427f6bd
