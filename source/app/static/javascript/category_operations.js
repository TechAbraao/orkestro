$(document).ready(function(){
    const editMenuSection = $(".w-full.h-full.bg-green-400");
    const btnCreateCategory = $("#btn-create-category")
    const modalCreateCategory = $("#modalCreateCategory");

    function loadCategories() {
        $.ajax({
            url: getCategoriesURL,
            method: "GET",
            success: function (res) {
                console.log("Response: ", res);
                editMenuSection.empty();

                if(res.success && res.data.length > 0){
                    const gridContainer = $('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4"></div>');
                    editMenuSection.append(gridContainer);

                    res.data.forEach(category => {
                        const categoryCard = $(`
                            <div class="bg-white rounded-xl shadow-lg p-5 flex flex-col justify-between hover:scale-105 transform transition-all duration-300">
                                <div>
                                    <h3 class="text-xl font-bold text-gray-800 mb-2">${category.name}</h3>
                                    <p class="text-gray-600 mb-4">${category.description}</p>
                                </div>
                                <div class="flex justify-end gap-2">
                                    <button class="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded font-semibold edit-btn">
                                        Editar
                                    </button>
                                    <button class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded font-semibold delete-btn" data-id="${category.id}">
                                        Excluir
                                    </button>
                                </div>
                            </div>
                        `);
                        gridContainer.append(categoryCard);
                    });
                } else {
                    editMenuSection.html("<p class='text-gray-700 p-4'>Nenhuma categoria encontrada.</p>");
                }
            },
            error: function (xhr) {
                let response = JSON.parse(xhr.responseText);
                console.error("Error: ", response);
            }
        });
    }
    loadCategories();
    editMenuSection.on("click", ".delete-btn", function() {
        const categoryId = $(this).data("id");
        const deleteCategoryURL = `/api/categories/${categoryId}`;

        if(confirm("Tem certeza que deseja excluir esta categoria?")) {
            $.ajax({
                url: deleteCategoryURL,
                method: "DELETE",
                success: function(res) {
                    if(res.success){
                        alert("Categoria excluída com sucesso!");
                        window.location.reload();
                        loadCategories();
                    } else {
                        alert("Erro ao excluir categoria: " + res.message);
                    }
                },
                error: function(xhr) {
                    let response = JSON.parse(xhr.responseText);
                    console.error("Error: ", response);
                    alert("Erro ao excluir categoria.");
                }
            });
        }
    });


    btnCreateCategory.click(function() {
        modalCreateCategory.removeClass("hidden");
    });

    $("#closeModal, #cancelCreateCategory").click(function() {
        modalCreateCategory.addClass("hidden");
        $("#formCreateCategory")[0].reset();
    });

    const btnConfirmCreateCategory = $("#btn-confirm-create-category")
    btnConfirmCreateCategory.click(function () {
        let categoryName = $("#categoryName").val()
        let categoryDescription = $("#categoryDescription").val()

         $.ajax({
            url: getCategoriesURL,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                name: categoryName,
                description: categoryDescription
            }),
            success: function () {
                console.log("Categoria criada com sucesso!");
                window.location.reload()

            },
            error: function (xhr) {
                let response = JSON.parse(xhr.responseText);
                console.error("Error: ", response);
                console.error("Erro ao criar categoria.");
            }
        });
    })
});
