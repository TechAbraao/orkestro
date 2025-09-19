$(document).ready(function () {
    $.ajax({
        url: "/api/stores/me",
        method: "GET",
        success: function (response) {
            console.log("User Infos:", response);
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseText);
        }
    });
});
