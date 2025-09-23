function createMenuCard(menu) {
    return `
    <div class="bg-white rounded-md shadow-md p-6 w-64 h-64 hover:shadow-xl transition-shadow duration-300 flex flex-col justify-between">
        <button 
            class="btn-delete-menu px-3 py-1 rounded-md bg-red-500 text-white text-sm font-medium 
         hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 
         transition-colors duration-200 shadow-sm" 
            data-id="${menu.id}">
            Excluir
        </button>
        <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-1 capitalize">${menu.name}</h3>
            <p class="text-sm text-indigo-600 mb-2 truncate">${menu.slug}</p>
            <p class="text-gray-700 text-sm line-clamp-3">${menu.description}</p>
        </div>
        <div class="mt-2 flex flex-col gap-2">
            <p class="text-xs text-gray-400">Criado em: ${menu.created_at ? menu.created_at.slice(0, 10) : "N/A"}</p>
            <a href="/stores/${menu.slug}" 
               class="px-3 py-1 rounded-md bg-indigo-600 text-white text-sm font-medium
                      hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition text-center">
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

    $(document).on("click", ".btn-delete-menu", function() {
        const menuId = $(this).data("id");
        console.log("Excluir menu:", menuId);
    });
});
