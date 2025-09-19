const sidebar = document.getElementById("sidebar");
const toggleBtn = document.getElementById("toggle-btn-sidenav");
const sidebarTexts = document.querySelectorAll(".sidebar-text");
const sidebarTitle = document.getElementById("sidebar-title");
const toggleBtnIcon = document.getElementById('toggle-btn-sidenav-icon');

toggleBtn.addEventListener("click", () => {
    const isExpanded = sidebar.classList.toggle("w-64");
    sidebar.classList.toggle("w-16");

    sidebarTexts.forEach(text => text.classList.toggle("hidden"));
    sidebarTitle.classList.toggle("hidden");

    toggleBtnIcon.src = isExpanded
        ? '/static/icons/left-arrow.png'
        : '/static/icons/right-arrow.png';

    document.querySelectorAll("nav a").forEach(link => link.classList.toggle("justify-center "));
});

document.addEventListener("DOMContentLoaded", () => {
    const settingsBtn = document.getElementById("settings-btn");
    const settingsSubmenu = document.getElementById("settings-submenu");
    const settingsArrow = document.getElementById("settings-arrow");

    settingsBtn.addEventListener("click", (e) => {
        e.preventDefault();
        settingsSubmenu.classList.toggle("hidden");
        settingsArrow.classList.toggle("rotate-180");
    });
});
