$(document).ready(function(){


  //AJAX call on registering a user
  $('#signup').submit(function() {
    if ($('#password-signup').val() !== $('#password-conf-signup').val()) {
      //TODO: create proper validation messages tooltips
      alert('Passwords do not match!');
      return;
    }
    type = $(this).attr('method');
    url = $(this).attr('action');
    data = $(this).serializeArray();
    signupAndLoginAJAX(type, url, data);
    return false;
  });

  //AJAX call on attempting to log a user on
  $('#login').submit(function() {
    type = $(this).attr('method');
    url = $(this).attr('action');
    data = $(this).serializeArray();
    signupAndLoginAJAX(type, url, data);
    return false;
  });

  function signupAndLoginAJAX(type, action, data) {
    $.ajax({
      type: type,
      url: action,
      data: data,
      success: function(data) {
        if (data.status == 1) {
          window.location.replace(data.url);
        } else {
          alert(data.message);
        }
      },
      error: function(data) {
        alert("error");
      }
    });
  }

  $('#signup-switch').click(function() {
    $('#signup').addClass('hidden');
    $('#login').removeClass('hidden');
  });

  $('#login-switch').click(function() {
    $('#login').addClass('hidden');
    $('#signup').removeClass('hidden');
  });
});
