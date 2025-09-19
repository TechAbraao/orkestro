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
                let successMessage = response.message || "Login successful";

                $("aside .alert_base_login_success .alert_login_store_success").text(successMessage);
                $("aside .alert_base_login_success").removeClass("hidden");

                setTimeout(() => {
                    $("aside .alert_base_login_success").addClass("hidden");
                }, 2300);

                setTimeout(function () {
                    window.location.href = "/dashboard";
                }, 2300)
            },
            error: function (xhr) {
                let errorMessage = "";
                try {
                    let response = JSON.parse(xhr.responseText);

                    if (response.errors) {
                        if (typeof response.errors === "string") {
                            errorMessage = response.errors;
                        } else {
                            for (let field in response.errors) {
                                errorMessage += `${response.errors[field].join(", ")}\n`;
                            }
                        }
                    } else if (response.message) {
                        errorMessage = response.message;
                    } else {
                        errorMessage = "An unknown error occurred.";
                    }

                } catch (e) {
                    errorMessage = xhr.responseText;
                }

                $("aside .alert_base_login_error .alert_login_store_error").text(errorMessage);
                $("aside .alert_base_login_error").removeClass("hidden");

                setTimeout(() => {
                    $("aside .alert_base_login_error").addClass("hidden");
                }, 4000)
            }
        });
    })
})