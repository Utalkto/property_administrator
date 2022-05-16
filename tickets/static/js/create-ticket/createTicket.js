let tenantId = 0;
let ticketType = 0;


function nextStage(_nextStage, optionSelected, branchSelected){

    jsonData = {
        'branch_selected': branchSelected,
        'next_stage': _nextStage,
        'option_selected': optionSelected,
        'ticket_id': $('#ticket-id').val(),
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
    }

    $.ajax({
        type: 'POST',
        url: '/tickets/stage-info/',
        data: jsonData,
        success: function (response) {
            
            if (response.completed == true) {
                window.location.href = `http://localhost:8000/tickets/ticket-info/${$('#ticket-id').val()}`;
            }

            
            addFields(response);

        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
            console.log(response.serializer_error);
        }
    });

}


function addFields(data){

    $('#buttons-section').remove();

    $('#section-fields').append(
        `
        <div class="row" id="buttons-section">
        </div>
        `
    );
    
    n = 0;
    Object.entries(data.form_fields).forEach(([key, value]) => {


    $('#buttons-section').append(
        `
        <div class="col-lg-6">
            <div class="form-group" id=space-btn${n}>
            
            </div>
        </div>
        `
    );

    $(`#space-btn${n}`).append(
        btn = $(document.createElement('button')).prop({
            type: 'button',
            innerHTML: value.string,
            class: 'form-control',
            style: 'cursor: pointer;',
        })
    );

    btn.click( function() {

        nextStage(data.current_stage, optionSelected=value.id, branchSelected=data.branch_selected);

    })
        
    
    n++;

    });

    $('#section-name').text(data.stage_title)


    console.log('created');

    

}


// In dashboard creation 


function getNextInfo(_nextStage, option_id) {

    jsonData = {
        'next_stage': _nextStage,
        'option_id': option_id
    }
    
    if (_nextStage == 3) {
        tenantId = option_id;
    }

    if (_nextStage == 4) {
        ticketType = option_id;
    }

    if (_nextStage == 5) {
        jsonData['tenant_id'] = tenantId
        jsonData['ticket_type'] = ticketType
    }



    $.ajax({
        type: 'GET',
        url: '/tickets/create-ticket-main-info/',
        data: jsonData,
        success: function (response) {

            if (_nextStage == 5) {

                window.location.href = `http://localhost:8000/tickets/ticket-info/${3}`;
                
            } 
            else {
            
                addNextInfoInCrationDashboard(response, _nextStage++);
                
            }
            

        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
            console.log(response.serializer_error);
        }
    });

}


function addNextInfoInCrationDashboard(data, _nextStage){

    $('#cards-section-inner').remove();

    $('#cards-section').append(
        `
        <div class="row" id="cards-section-inner">
        </div>
        `
    );
    
    n = 0;
    Object.entries(data.options).forEach(([key, value]) => {

    // <img class="img-fluid" src="${value.img.url}" alt=""></img>
    // it be great if we put a main img in units t
    let titleToShow = '';
    let numberToShow = '';


    if (data.next_stage >= 4){
        titleToShow = value.string_part;
    }
    else if (data.next_stage == 3){
    } 
    else if (data.next_stage == 2){
        numberToShow += `Number of residentns: ${value.number_of_residents}`
        
    } 
    
    if (data.next_stage <= 3 ){
        titleToShow = value.name;
    }


    
    $('#cards-section-inner').append(
        `
        <div class="col-md-6 col-lg-3">
            <div class="card">
            
                <div class="card-body">
                    <h5 class="card-title">${titleToShow}</h5>
                    <p class="card-text"> <strong>Address :</strong> ${value.address} </p>
                </div>
                <div class="card-footer" id=card-btn${n}>
                    <p class="card-text d-inline"><small class="text-muted">${numberToShow}</small></p>
                </div>

            </div>
        </div>
        `
    );

    $(`#card-btn${n}`).append(
        btn = $(document.createElement('button')).prop({
            type: 'button',
            innerHTML: '<small>Select</small>',
            class: 'card-link float-right',
            style: 'cursor: pointer; border:none; background: none;',
        })
    );

    btn.click( function() {

        getNextInfo(_nextStage=data.next_stage, option_id=value.id);

    })
        
    
    n++;

    });

    $('#stage-name').text(data.stage_title)


}