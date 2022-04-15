// For register page styling
$(document).ready(function() {

    // Placeholders for register inputs
    $('input').addClass('form-control');
    $('#id_first_name').attr('placeholder','First Name');
    $('#id_last_name').attr('placeholder','Last Name');
    $('#id_username').attr('placeholder','Username');
    $('#id_email').attr('placeholder','Email Address');
    $('#id_password1').attr('placeholder','Password');
    $('#id_password2').attr('placeholder','Confirm Password');

    $('#id_password1').addClass('form-control');
    $('#id_password2').addClass('form-control');

    $('#id_content').addClass('mb-4');

    // for user create form
    $('#id_email').addClass('form-control');
    $('#id_image').removeClass('form-control');
    $('#id_image').removeAttr('required');
    $('#group-select').removeAttr('required');

    $('select[type="date"]').addClass('form-control');
    $('select[name="date_month"]').addClass('col-5');
    $('select[name="date_day"]').addClass('col-3');
    $('select[name="date_year"]').addClass('col-4');

    $('input[type="time"]').addClass('form-control');

    $('#id_image').after('<br>');


    $('#group-delete-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var groupid = button.data('id')
        var modal = $(this)
        modal.find('.modal-body #group-delete-id').val(groupid)
    })

    $('#user-delete-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var userid = button.data('id')
        var modal = $(this)
        modal.find('.modal-body #user-delete-id').val(userid)
    })
    
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })
    
});
