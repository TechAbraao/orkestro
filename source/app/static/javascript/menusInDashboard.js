
function createMenuCard(menu) {
    return `
    <div class="menu-card bg-white rounded-2xl border-2 border-gray-300  transition-shadow duration-300 flex flex-col justify-between h-80 w-[360px] p-6">
        <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-bold text-gray-900 capitalize">${menu.name}</h3>
            ${currentUserRoles?.includes("PRIVILEGED") || currentUserRoles.includes("ADMIN") ? `
                <button 
                    title="Excluir"
                    class="btn-delete-menu px-3 py-1 rounded-full bg-red-500 text-white text-sm font-semibold
                       hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 transition"
                    data-id="${menu.id}">
                    Excluir
                </button>
                ` : `
                <button 
                    title="Permissão insuficiente"
                    disabled
                    class="px-3 py-1 rounded-full bg-gray-300 text-gray-500 text-sm font-semibold
                    cursor-not-allowed opacity-70">
                Excluir
                </button>
                `
                }
        </div>
        <p class="text-sm text-indigo-600 mb-2 truncate font-medium">${menu.slug}</p>
        <p class="text-gray-700 text-sm line-clamp-4 mb-2">${menu.description}</p>
        <div class="flex items-center gap-2">
            <span class="text-gray-700 text-sm line-clamp">Tipo:</span>
            <p class="text-gray-900 text-[14px] font-semibold line-clamp-4 bg-gray-200 rounded-full pl-3 pr-3">${menu.roles}</p>
        </div>
        
        <div class="mt-auto flex flex-col gap-1 h-[38%]">
            <a href="/menus/${menu.slug}" target="_blank"
                title="Cardápio"
                class="flex items-center justify-center bg-[#111111] hover:bg-[#050505] text-white transition-colors h-1/2 text-center
                font-semibold px-3 py-1 rounded-3xl transition-all w-full">
                    Acessar Cardápio
            </a>
            <a href="/menus/${menu.id}/categories" 
                title="Configurações"
                class="flex items-center justify-center bg-gray-200 hover:bg-gray-300 font-semibold h-1/2 text-center
                text-gray-700 px-3 py-1 rounded-3xl transition-colors w-full">
                    Configurações
            </a>
            
            <!--
            <p class="text-xs text-gray-400">Criado em: ${menu.created_at ? menu.created_at.slice(0, 10) : "N/A"}</p>
            -->
       
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

