function createMenuCard(menu) {
    return `
    <div class="menu-card bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-shadow duration-300 flex flex-col justify-between h-72 w-72 p-6">
        
        <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-bold text-gray-900 capitalize">${menu.name}</h3>
            <button 
                class="btn-delete-menu px-3 py-1 rounded-full bg-red-500 text-white text-sm font-semibold
                       hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 transition"
                data-id="${menu.id}">
                Excluir
            </button>
        </div>
        
        <p class="text-sm text-indigo-600 mb-2 truncate font-medium">${menu.slug}</p>
        <p class="text-gray-700 text-sm line-clamp-4 mb-4">${menu.description}</p>
        
        <div class="mt-auto flex flex-col gap-3">
            <p class="text-xs text-gray-400">Criado em: ${menu.created_at ? menu.created_at.slice(0, 10) : "N/A"}</p>
            
            <a href="/menus/${menu.id}/categories" 
                class="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium text-center
                hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition">
                Editar Cardápio
            </a>
            <a href="/menus/${menu.slug}" 
               class="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium text-center
                      hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition">
                Ver Cardápio
            </a>
        </div>
    </div>
    `;
}

$(document).ready(function () {
    $.ajax({
        url: `/api/menus?mine=true`,
        method: "GET",
        dataType: "json",
        success: function (menus) {
            const container = $("#menusContainer");
            container.empty();
            menus.data.forEach(menu => {
                container.append(createMenuCard(menu));
            });
        },
        error: function (xhr) {
            let response = JSON.parse(xhr.responseText);
            console.error("Error: ", response);
        }
    });
});

$(document).on("click", ".btn-delete-menu", function () {
    const menuId = $(this).data("id");

    const confirmDeleteModal = $("#modalConfirmOperation")
    confirmDeleteModal.removeClass("hidden");


    const btnConfirmDelete = $("#btn-confirm-op-delete")

    btnConfirmDelete.on("click", function () {
        $.ajax({
            url: `/api/menus/${menuId}`,
            method: "DELETE",
            success: function (response) {
                $(`.btn-delete-menu[data-id='${menuId}']`).closest(".menu-card").remove();
                window.location.reload()
            },
            error: function (xhr) {
                let response = {};
                try {
                    response = JSON.parse(xhr.responseText);
                } catch (e) {
                }
                alert(response.message || "Erro ao excluir o menu.");
                console.error("Error: ", response);
            }
        });
    })

});

