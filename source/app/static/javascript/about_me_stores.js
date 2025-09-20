$(document).ready(function () {
    $.ajax({
        url: aboutMeStore,
        method: "GET",
        success: function (response) {
            // console.log("User Infos:", response);
            if (response) {
                let storeName = response.data.name
                let storeTelephone = response.data.telephone
                let storeEmail = response.data.email
                let storeLogoURL = response.data.logo_url

                let storeNameNavbar = $("#store-name-navbar").text(storeName)
                let storeProfileName = $("#store-profile-name").text(storeName)
                let storeProfileTelephone = $("#store-profile-telephone").text(storeTelephone)
                let storeProfileEmail = $("#store-profile-email").text(storeEmail)
                $("img[alt='Store Logo']").attr("src", storeLogoURL);
            }
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseText);
        }
    });
});
