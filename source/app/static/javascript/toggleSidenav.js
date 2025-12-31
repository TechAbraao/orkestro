const sidebar = document.getElementById("sidebar");
const toggleBtn = document.getElementById("toggle-btn-sidenav");
const sidebarTexts = document.querySelectorAll(".sidebar-text");
const sidebarTitle = document.getElementById("sidebar-title");
const toggleBtnIcon = document.getElementById('toggle-btn-sidenav-icon');
const containerPhoto = $(".container-account-photo")
const containerTextCount = $(".container-text-count-orders-sidenav")

function toggleSidebar(expand) {
    const isExpanded = expand ?? !sidebar.classList.contains("w-64");

    if (!isExpanded) {
        containerPhoto.hide();
        containerTextCount.hide();
    } else {
        containerPhoto.show();
        containerTextCount.show();
    }

    sidebar.classList.toggle("w-64", isExpanded);
    sidebar.classList.toggle("w-16", !isExpanded);

    sidebarTexts.forEach(text => text.classList.toggle("hidden", !isExpanded));
    sidebarTitle.classList.toggle("hidden", !isExpanded);

    toggleBtnIcon.src = isExpanded
        ? '/static/icons/left-arrow.png'
        : '/static/icons/right-arrow.png';

    document.querySelectorAll("nav a").forEach(link => link.classList.toggle("justify-center ", !isExpanded));
}

toggleBtn.addEventListener("click", () => toggleSidebar());

function handleMenuClick(submenu, arrow) {
    if (sidebar.classList.contains("w-16")) {
        toggleSidebar(true);
    }

    const isOpen = submenu.classList.toggle("open");
    arrow.classList.toggle("rotate-180", isOpen);
}

document.addEventListener("DOMContentLoaded", () => {
    const settingsBtn = document.getElementById("settings-btn");
    const settingsSubmenu = document.getElementById("settings-submenu");
    const settingsArrow = document.getElementById("settings-arrow");

    const statisticsBtn = document.getElementById("statistics-btn");
    const statisticsSubmenu = document.getElementById("statistics-submenu");
    const statisticsArrow = document.getElementById("statistics-arrow");

    settingsBtn.addEventListener("click", (e) => {
        e.preventDefault();
        handleMenuClick(settingsSubmenu, settingsArrow);
    });

    statisticsBtn.addEventListener("click", (e) => {
        e.preventDefault();

        handleMenuClick(statisticsSubmenu, statisticsArrow);
    });
});
