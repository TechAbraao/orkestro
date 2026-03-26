$(document).ready(function () {
    $.ajax({
        url: "/api/stores",
        method: "GET",
        success: function(response) {
            let responseParsed = JSON.stringify(response.data)
            console.log(`Resposta da API: ${responseParsed}`)
        },
        error: function() {

        }
    })


    $("form").on("submit", function (e) {
        e.preventDefault();

        let storeName = $("#storeName").val();
        let email = $("#email").val();
        let password = $("#password").val();
        let telephone = $("#telephone").val();
        let role = $("#role_store").val();
        let roleList = [role]
        console.log(roleList)


        $.ajax({
            url: "/api/stores",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                name: storeName,
                email: email,
                password: password,
                telephone: telephone,
                roles: roleList
            }),

            success: function (response) {
                console.log("Success:", response);

                let successMessage = response.message || "Account created successfully";
                $("aside .alert_base_register_success .alert_register_store_success").text(successMessage);
                $("aside .alert_base_register_success").removeClass("hidden");

                setTimeout(() => {
                    $("aside .alert_base_register_success").addClass("hidden");
                }, 4000);
            },
            error: function (xhr) {
                let errorMessage = "";
                try {
                    let response = JSON.parse(xhr.responseText);

                    if (response.errors) {
                        for (let field in response.errors) {
                            errorMessage += `${response.errors[field].join(", ")}\n`;
                        }
                    } else if (response.message) {
                        errorMessage = response.message;
                    } else {
                        errorMessage = "An unknown error occurred.";
                    }

                } catch (e) {
                    errorMessage = xhr.responseText;
                }
                $("aside .alert_base_register_error .alert_register_store_error").text(errorMessage);
                $("aside .alert_base_register_error").removeClass("hidden");

                setTimeout(() => {
                    $("aside .alert_base_register_error").addClass("hidden");
                }, 4000)
            }
        });
    });
});
