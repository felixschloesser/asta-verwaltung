document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');


        // Invert the color of the Admin Button
        const $adminButton = document.getElementById('admin-button');
        $adminButton.classList.toggle('is-dark');
      });
    });


  }


  // Make rows clickable
  const $rows = document.querySelectorAll("tr[data-href]");

  $rows.forEach(row => {
    row.addEventListener("click", () => {
      window.location.href = row.dataset.href;
    });
  });


  // Enable print buttons to print the page
  const $printButton = document.getElementById('print');
  $printButton.onclick = function () { window.print(); };

});
