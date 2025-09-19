$(document).ready(function () {
    $.ajax({
        url: "/api/stores/me",
        method: "GET",
        success: function (response) {
            console.log("User info:", response);
        },
        error: function (xhr) {
            console.error("Erro ao buscar usuário:", xhr.responseText);
        }
    });
});
