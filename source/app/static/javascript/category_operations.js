$(document).ready(function(){
    const categoriesContainer = $("#categoriesContainer");
    const btnCreateCategory = $("#btn-create-category");
    const modalCreateCategory = $("#modalCreateCategory");

    function loadCategories() {
        $.ajax({
            url: getCategoriesURL,
            method: "GET",
            success: function (res) {
                console.log("Response: ", res);
                categoriesContainer.empty();

                if(res.success && res.data.length > 0){
                    res.data.forEach(category => {
                        const categoryCard = $(`
                            <div class="bg-white rounded-xl h-48 shadow-lg p-5 flex flex-col justify-between hover:scale-105 transform transition-all duration-300">
                                <div>
                                    <h3 class="text-xl font-bold text-gray-800 mb-2">${category.name}</h3>
                                    <p class="text-gray-600 mb-4">${category.description}</p>
                                </div>
                                <div class="flex justify-end gap-2">
                                    <button class="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded font-semibold edit-btn">
                                        Editar
                                    </button>
                                    <button class="delete-btn bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded font-semibold" data-id="${category.id}">
                                        Excluir
                                    </button>
                                </div>
                            </div>
                        `);
                        categoriesContainer.append(categoryCard);
                    });
                } else {

                }
            },
            error: function (xhr) {
                console.error("Error: ", xhr.responseText);
            }
        });
    }

    loadCategories();

    categoriesContainer.on("click", ".delete-btn", function() {
        const categoryId = $(this).data("id");
        const deleteCategoryURL = `/api/categories/${categoryId}`;


        const confirmDeleteModal = $("#modalConfirmOperation")
        confirmDeleteModal.removeClass("hidden");
        const btnConfirmDeleteCategory = $("#btn-confirm-category-delete")

        btnConfirmDeleteCategory.on("click", () => {
            $.ajax({
                url: deleteCategoryURL,
                method: "DELETE",
                success: function (res) {
                    if (res.success) {
                        alert("Categoria excluída com sucesso!");
                        loadCategories();
                        window.location.reload()
                    } else {
                        alert("Erro ao excluir categoria: " + res.message);
                    }
                },
                error: function (xhr) {
                    console.error("Error: ", xhr.responseText);
                    alert("Erro ao excluir categoria.");
                }
            });
        })
    });

    btnCreateCategory.click(function() {
        modalCreateCategory.removeClass("hidden");
    });

    $("#closeModal, #cancelCreateCategory").click(function() {
        modalCreateCategory.addClass("hidden");
        $("#formCreateCategory")[0].reset();
    });

    const btnConfirmCreateCategory = $("#btn-confirm-create-category");
    btnConfirmCreateCategory.click(function () {
        let categoryName = $("#categoryName").val();
        let categoryDescription = $("#categoryDescription").val();

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
                modalCreateCategory.addClass("hidden");
                $("#formCreateCategory")[0].reset();
                loadCategories();
            },
            error: function (xhr) {
                console.error("Error: ", xhr.responseText);
                console.error("Erro ao criar categoria.");
            }
        });
    });
});
