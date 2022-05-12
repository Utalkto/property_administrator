function nextStage(_nextStage, optionSelected, branchSelected){

    jsonData = {
        'branch_selected': branchSelected,
        'next_stage': _nextStage,
        'option_selected': optionSelected,
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
    }

    $.ajax({
        type: 'POST',
        url: '/tickets/stage-info/',
        data: jsonData,
        success: function (response) {
            
            addFields(response);

        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
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