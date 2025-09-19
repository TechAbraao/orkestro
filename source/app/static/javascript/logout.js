$(document).ready(function () {
    $("#btn-logout").click(function () {
        fetch(logoutURL)
            .then(() => {
                window.location.href = "/signin";
            })
            .catch((err) => {
                console.error("Logout error:", err);
            });
    });
});