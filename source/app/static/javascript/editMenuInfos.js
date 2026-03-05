$(document).ready(function() {
    const btnOpenEditMenu = $("#btn-edit-menu-open");

    btnOpenEditMenu.on("click", function() {
        const modalEditMenu = $("#modalEditMenuModal")
        const btnEditMenu = $("#btn-edit-menu")
        modalEditMenu.removeClass("hidden")

        $.ajax({
            method: "GET",
            url: `/api/menus?mine=true`,
            success: function (response) {
                console.log(response.data);

                let currentMenuName = response.data[0].name
                let currentMenuDescription = response.data[0].description
                let currentMenuRoles = response.data[0].roles

                console.log(
                    `Name: ${currentMenuName} | Description: ${currentMenuDescription} | Roles: ${currentMenuRoles}`
                )

                let menuNameEdited = $("#menu_name_edit").val(currentMenuName)
                let menuDescriptionEdited = $("#menu_description_edit").text(currentMenuDescription)
                let menuRolesEdited = $("#role_menu_edit").val(currentMenuRoles)
            },
            error: function (xhr) {
                const errorDescription = xhr.responseText
                console.error(errorDescription)
            }
        })


        btnEditMenu.on("click", function() {
            let menuNameEdited = $("#menu_name_edit").val()
            let menuDescriptionEdited = $("#menu_description_edit").val()
            let menuRolesEdited = $("#role_menu_edit").val()

            $.ajax({
                method: "PUT",
                url: `/api/menus/${menuId}`,
                contentType: "application/json",
                data: JSON.stringify({
                    name: menuNameEdited,
                    description: menuDescriptionEdited,
                    roles: menuRolesEdited
                }),
                success: function(response) {
                    console.log(response)
                },
                error: function(xhr) {
                    const errorDescription = xhr.responseText
                    console.error(errorDescription)
                }
            })
        })
    })
})