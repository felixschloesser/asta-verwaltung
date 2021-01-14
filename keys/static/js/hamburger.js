$(document).ready(function() {

  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function() {

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
      $(".admin-button").toggleClass("is-dark");

  });
});


$(document).ready(function() {

  // Check for click events on the navbar burger icon
  $(".message-delete").click(function() {
      // Delete the ".message" div from the dom
      $( ".message" ).remove();
  });
});
