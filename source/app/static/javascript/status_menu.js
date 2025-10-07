$(document).ready(function() {
    const btnStatusMenu = $("#btn-status-menu")
    const modalChangeStatus = $("#modalMenuStatus")

    btnStatusMenu.on("click", () => {
        modalChangeStatus.removeClass("hidden")
    })
})