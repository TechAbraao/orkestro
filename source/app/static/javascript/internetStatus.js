document.addEventListener("DOMContentLoaded", () => {
    const internetStatus = document.getElementById("internetStatus");

    function checkInternet() {
        if (!navigator.onLine) {
            internetStatus.classList.remove("invisible");
            internetStatus.classList.add("visible");
        } else {
            internetStatus.classList.remove("visible");
            internetStatus.classList.add("invisible");
        }
    }
    setInterval(checkInternet, 2000);
    window.addEventListener("online", checkInternet);
    window.addEventListener("offline", checkInternet);
    checkInternet();
});
