$(document).ready(function(){

  $("#tournament-date").datepicker({ dateFormat: 'yy-mm-dd' });

  $('#create-tournaments').submit(function() {
    $.ajax({
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      data: $(this).serializeArray(),
      success: function(data) {
        if (data.status == 1) {
          window.location.replace(data.url);
        } else {
          alert(data.message);
        }
      },
      error: function(xhr) {
        console.log(xhr);
      }
    });
    return false;
  });
});
