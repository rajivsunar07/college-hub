
$(document).ready(function(){
    $('#post-delete-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var postid = button.data('id')
        var modal = $(this)
        modal.find('.modal-body #post-delete-id').val(postid)
    })
})

