$(document).ready(function(){
  $('#add-members').submit(function() {
    $.ajax({
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      data: $(this).serializeArray(),
      success: function(data) {
        alert(data.message);
      },
      error: function(xhr) {
        console.log(xhr);
      }
    });
    return false;
  });
});
