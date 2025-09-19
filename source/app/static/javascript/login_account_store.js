$(document).ready(function () {
    $("form").on("submit", function (e) {
        e.preventDefault();

        let email = $("#email").val();
        let password = $("#password").val();

       $.ajax({
            url: loginURL,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                email: email,
                password: password,
            }),
            success: function (response) {
                console.log("Response: ", response)
            },
            error: function (xhr) {
                 let response = JSON.parse(xhr.responseText);
                 console.error("Error(s): ", response)
            }
        });

    })
})