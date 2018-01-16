$(document).ready(function() {
  $('.application-submit').click(function() {
    const form = $(this).parent();
    let data = form.serializeArray();
    data.push({name: this.name, value: this.value})
    $.ajax({
      type: form.attr('method'),
      url: form.attr('action'),
      data: data,
      success: function(data) {
        alert(data.message);
      },
      error: function(xhr) {
        console.log(xhr);
      }
    });
    return false;
  });

  $('#team-apply').submit(function() {
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
