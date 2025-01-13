$(document).ready(function () {
    $("#navbarToggler").click(function () {
        $("#navbarNav").toggleClass("show");
    });
});
document.getElementById('currentYear').textContent = new Date().getFullYear();