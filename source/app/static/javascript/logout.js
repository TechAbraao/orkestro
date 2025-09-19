$(document).ready(function () {
    $("#btn-logout").click(function () {
        document.getElementById('logoutModal').classList.remove('hidden');
        $("#btn-confirm-logout").click(function () {
            fetch(logoutURL)
                .then(() => {
                    window.location.href = "/signin";
                })
                .catch((err) => {
                    console.error("Logout error:", err);
                });
        })
    });
});