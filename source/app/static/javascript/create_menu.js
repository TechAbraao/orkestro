$(document).ready(function () {
    const modal = $("#modalCreateMenuModal");
    const btnOpenModal = $("#btn-open-modal-create-menu");
    const btnCreateMenu = $("#btn-create-menu");

    btnOpenModal.click(function () {
        modal.removeClass("hidden");
    });

    modal.click(function (e) {
        if ($(e.target).is("#modalCreateMenuModal")) {
            modal.addClass("hidden");
        }
    });
    btnCreateMenu.click(function (e) {
        e.preventDefault();

        let menuName = $("#menu_name").val();
        let menuDescription = $("#menu_description").val();

        $.ajax({
            url: "/api/menus",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                name: menuName,
                description: menuDescription
            }),
            success: function () {
                console.log("Menu criado com sucesso!");
                modal.addClass("hidden");
                $("#menu_name").val("");
                $("#menu_description").val("");

                window.location.reload()

            },
            error: function () {
                console.error("Erro ao criar menu");
            }
        });
    });
});
