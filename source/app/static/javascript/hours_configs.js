$(document).ready(function () {
    btnHoursConfig = $("#btn-hours-config")
    modalOpeningHours = $("#modalOpeningHours")

    btnHoursConfig.on("click", () => {
        modalOpeningHours.removeClass("hidden")
    })
})