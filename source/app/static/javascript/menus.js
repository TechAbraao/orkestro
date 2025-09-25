let menuNameHTML = $("#menu-name")
let menuDescriptionHTML = $("#menu-description")
let btnContactMenu = $("#btn-contact-menu")

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
    $.ajax({
        url: aboutMeStore,
        method: "GET",
        success: function (response) {
            console.log("User Infos:", response);
            if (response) {

                let storeLogoURL = response.data.logo_url
                $("img[alt='Store Logo']").attr("src", storeLogoURL);
            }
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseText);
        }
    });

    btnContactMenu.click(() => {
        $("#modalContactMenuModal").removeClass("hidden");
    });

    $("#modalContactMenuModal button").click(() => {
        $("#modalContactMenuModal").addClass("hidden");
    });
})
