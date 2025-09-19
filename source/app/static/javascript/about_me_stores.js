$(document).ready(function () {
    $.ajax({
        url: aboutMeStore,
        method: "GET",
        success: function (response) {
            // console.log("User Infos:", response);
            if (response) {
                let storeName = response.data.name
                // console.log(storeName)
                let storeNameNavbar = $("#store-name-navbar").text(storeName)

            }
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseText);
        }
    });
});
