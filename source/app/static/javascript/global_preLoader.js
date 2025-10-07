$(document).ajaxStart(function () {
    $('#preloader').removeClass('hidden');
});

$(document).ajaxStop(function () {
    $('#preloader').addClass('hidden');
});