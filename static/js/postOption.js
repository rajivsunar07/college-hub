// ajax for postoptions
  $(document).ready(function(){
    $(".optionButton").click(function(e){
      e.preventDefault();
      $.ajax({
          type:'POST',
          url: '/blog/post/choose/',
          data: {
            option: this.id,
            pk: $('input[name=PostId]').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          dataType: 'json',
          success:function(response){
            var postid = "#" + response['pk'].toString();
            $(postid).html(response['form']);
          }
      })
    })
})
