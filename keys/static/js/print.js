document.addEventListener('DOMContentLoaded', () => {
  // Enable print buttons to print the page
  const $printButton = document.getElementById('print');
  $printButton.onclick = function () {
        let original_title = document.title;
        var h1Text = document.querySelector(".title").textContent;
        document.title = h1Text + " - Übersicht";
        window.print();
        document.title = original_title
    };
});
