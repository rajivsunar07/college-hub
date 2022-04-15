$(document).ready(function(){

    $('#comment-update-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var commentid = button.data('id')
        var commentcontent = button.data('content')
        var modal = $(this)
        modal.find('.modal-body #comment-update-id').val(commentid)
        modal.find('.modal-body #comment-update-content').val(commentcontent)
    })

    $('#comment-delete-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var commentid = button.data('id')
        var modal = $(this)
        modal.find('.modal-body #comment-delete-id').val(commentid)
    })
})

