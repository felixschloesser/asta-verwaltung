document.addEventListener('DOMContentLoaded', () => {
  // Enable print buttons to print the page
  const $printButton = document.getElementById('print');
  $printButton.onclick = function () { window.print(); };
});
