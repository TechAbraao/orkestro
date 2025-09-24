let menuNameHTML = $("#menu-name")
let menuDescriptionHTML = $("#menu-description")


$(document).ready(function () {
    $.ajax({
        url: menuClient,
        method: "GET",
        success: function (res) {
            console.log("Response: ", res)

            let menuDescription = res.data.description;
            let menuName = res.data.name
            console.log("Name: ", menuName)
            console.log("Menu Description: ", menuDescription)

            menuNameHTML.text(menuName)
            menuDescriptionHTML.text(menuDescription)

        },
        error: function (xhr) {

        }
    })
})
