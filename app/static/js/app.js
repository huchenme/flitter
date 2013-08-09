$( document ).ready(function() {
  $("#new_post_field").on("keyup", function(e) {
    var max = parseInt($(this).attr("maxlength"));
    if ($(this).val().length > max) {
      $(this).val($(this).val().substr(0, $(this).attr("maxlength")));
    }
    $(".charsRemaining").html("" + (max - $(this).val().length));
    if ($(this).val().length > 0) {
      $('#submit').toggleClass('disabled', false);
    } else {
      $('#submit').toggleClass('disabled', true);
    }
  });
});