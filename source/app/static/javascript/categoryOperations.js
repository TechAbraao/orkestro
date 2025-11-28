$(document).ready(function () {
    const categoriesContainer = $("#categoriesContainer");
    const btnCreateCategory = $("#btn-create-category");
    const modalCreateCategory = $("#modalCreateCategory");

    window.toggleDropdown = function (id) {
        const dropdown = document.getElementById(`dropdown-${id}`);
        const arrow = document.getElementById(`arrow-${id}`);
        if (!dropdown || !arrow) return;
        dropdown.classList.toggle("hidden");
        arrow.classList.toggle("rotate-180");
    };
    let categoriesData = [];
    function loadCategories() {
        $.ajax({
            url: getCategoriesURL,
            method: "GET",
            success: function (res) {
                console.log("Response: ", res);
                categoriesContainer.empty();

                if (res.success && res.data.length > 0) {
                    res.data.forEach(category => {
                        categoriesData = res.data;
                        const categoryCard = $(`
                            <div
                                class="bg-gradient-to-b from-white to-gray-50 rounded-2xl h-auto w-full p-6
                                flex flex-col justify-between transform transition-all duration-300 border border-gray-100"
                            >
                                <div>
                                    <h3 class="text-2xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 
                                    bg-clip-text text-transparent mb-2">
                                        ${category.name}
                                    </h3>
                                    <!--
                                    <p class="text-gray-700 mb-4 leading-relaxed">
                                        ${category.description}
                                    </p>
                                    -->
                                </div>

                                <div class="flex justify-start gap-2 pb-3">
                                    <button
                                        id="btn-edit-category"
                                        data-id="${category.id}"
                                        class="px-5 py-3 bg-gray-900 text-base text-white rounded-3xl hover:bg-gray-800 font-bold"
                                    >
                                        Editar categoria
                                    </button>
                                    <button
                                        id="btn-add-product"
                                        class="px-5 py-3 bg-gray-900 text-base text-white rounded-3xl hover:bg-gray-800 font-bold"
                                        data-id="${category.id}"
                                    >
                                        Adicionar produto
                                    </button>
                                    <button
                                        class="delete-btn px-5 py-3 bg-red-500 text-base text-white rounded-3xl hover:bg-red-600 font-bold"
                                        data-id="${category.id}"
                                    >
                                        Excluir categoria
                                    </button>
                                </div>

                                <div class="relative mb-5">
                                    <button
                                        class="w-full bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 
                                        hover:to-indigo-600 text-white px-5 py-2.5 rounded-lg font-semibold 
                                        flex justify-between items-center shadow-md transition-all duration-300 hover:shadow-lg"
                                        onclick="toggleDropdown('${category.id}')"
                                    >
                                        <span>Conferir produtos</span>
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="h-5 w-5 transform transition-transform duration-300"
                                            id="arrow-${category.id}"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M19 9l-7 7-7-7"
                                            />
                                        </svg>
                                    </button>

                                    <div
                                        id="dropdown-${category.id}"
                                        class="hidden bg-gray-50 mt-3 rounded-xl shadow-inner p-4 space-y-3 
                                        border border-gray-200 transition-all duration-300"
                                    >
                                        <section class="w-full grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                            ${(category.products || [])
                                                .map(
                                                    product => `
                                                        <div class="flex justify-between h-52 items-center bg-white rounded-lg px-4 
                                                        py-3 shadow-sm hover:shadow-md transition-all duration-200 border border-gray-100">

                                                            <div class="w-1/2 rounded-2xl h-full bg-green-100 overflow-hidden flex items-center justify-center">
                                                                <img src="${product.image_url || ''}" alt="${product.name}" class="object-cover h-full w-full rounded-2xl">
                                                            </div>

                                                            <div class="w-1/2 flex flex-col h-full w-full p-2 justify-between">
                                                                <div>
                                                                    <span class="text-gray-800 font-medium text-lg block">${product.name}</span>
                                                                    <span class="text-sm text-gray-500 block">R$ ${product.price ? product.price.toFixed(2) : "0.00"}</span>
                                                                    <span class="text-sm text-gray-500 block">${product.description}</span>
                                                                </div>

                                                                <div class="flex justify-end gap-2 mt-3">
                                                                    <button id="btn-edit-product" data-id="${product.id}"
                                                                        class="bg-blue-500 hover:bg-blue-600 text-white text-sm px-3 py-1 rounded-md transition-all">
                                                                        Alterar
                                                                    </button>
                                                                    <button id="btn-delete-product" data-id="${product.id}"
                                                                        class="bg-red-500 hover:bg-red-600 text-white text-sm px-3 py-1 rounded-md transition-all">
                                                                        Excluir
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    `
                                                )
                                                .join("")}
                                        </section>
                                    </div>
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

    categoriesContainer.on("click", ".delete-btn", function () {
        const categoryId = $(this).data("id");
        const deleteCategoryURL = `/api/categories/${categoryId}`;
        const confirmDeleteModal = $("#modalConfirmCategory");
        confirmDeleteModal.removeClass("hidden");
        const btnConfirmDeleteCategory = $("#btn-confirm-category-delete");

        btnConfirmDeleteCategory.off("click").on("click", () => {
            $.ajax({
                url: deleteCategoryURL,
                method: "DELETE",
                success: function (res) {
                    if (res.success) {
                        loadCategories();
                        confirmDeleteModal.addClass("hidden")
                    } else {
                        alert("Erro ao excluir categoria: " + res.message);
                    }
                },
                error: function (xhr) {
                    console.error("Error: ", xhr.responseText);
                    alert("Erro ao excluir categoria.");
                }
            });
        });
    });

    btnCreateCategory.click(function () {
        modalCreateCategory.removeClass("hidden");
    });

    $("#closeModal, #cancelCreateCategory").click(function () {
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

    const modalAddProduct = $("#modalAddProduct");
    categoriesContainer.on("click", "#btn-add-product", function () {
        const categoryId = $(this).data("id");
        modalAddProduct.removeClass("hidden");

        $("#productName").focus();
        $("#btn-confirm-add-product").off("click").on("click", function (e) {
            e.preventDefault();

            let productName = $("#productName").val();
            let productPrice = parseFloat($("#productPrice").val());
            let productDescription = $("#productDescription").val();

            $.ajax({
                url: `/api/categories/${categoryId}/products`,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    name: productName,
                    price: productPrice,
                    description: productDescription
                }),
                success: function (res) {
                    console.log("Produto adicionado:", res);
                    modalAddProduct.addClass("hidden");
                    $("#formAddProduct")[0].reset();
                    loadCategories();
                },
                error: function (xhr) {
                    console.error("Erro ao adicionar produto:", xhr);
                    alert("Error: ", xhr);
                }
            });
        });
    });

    categoriesContainer.on("click", "#btn-delete-product", function () {
        const productId = $(this).data("id");
        console.log(`Your productId is ${productId}`)
        const modalConfirmOperationDeleteProduct = $("#modalConfirmProduct")
        const btnConfirmDeleteProduct = $("#btn-confirm-product-delete")
        modalConfirmOperationDeleteProduct.removeClass("hidden")


        btnConfirmDeleteProduct.off("click").on("click", () => {
            console.log(`Deletando produto com ID: ${productId}`);

            $.ajax({
                url: `/api/products/${productId}`,
                method: "DELETE",
                success: function (res) {
                    if (res.success) {
                        modalConfirmOperationDeleteProduct.addClass("hidden")
                        loadCategories();
                    } else {
                        console.warn(`Erro ao excluir produto ${productId}: ${res.message}`);
                        alert("Erro ao excluir produto.");
                    }
                },
                error: function (xhr) {
                    console.error(`Erro na requisição DELETE (status ${xhr.status}): ${xhr.responseText}`);
                    alert("Erro ao excluir produto.");
                }
            });
        });

    })

    categoriesContainer.on("click", "#btn-edit-category", function () {
        const categoryId = $(this).data("id");
        const modalEditCategory = $("#modalEditCategory");

        modalEditCategory.data("category-id", categoryId);
        modalEditCategory.removeClass("hidden");
    });

    categoriesContainer.on("click", "#btn-edit-product", function () {
        const productId = $(this).data("id");
        const modalEditProduct = $("#modalEditProduct");

        let selectedProduct = null;
        for (const category of categoriesData) {
            const found = category.products.find(p => p.id === productId);
            if (found) {
                selectedProduct = found;
                break;
            }
        }

        if (!selectedProduct) {
            alert("Produto não encontrado!");
            return;
        }

        $("#editProductName").val(selectedProduct.name);
        $("#editProductDescription").val(selectedProduct.description);
        $("#editProductPrice").val(selectedProduct.price);

        modalEditProduct.data("product-id", productId);

        modalEditProduct.removeClass("hidden");
        $("#editProductName").focus();
    });

    $("#btnConfirmEditCategory").on("click", function (event) {
        event.preventDefault();

        const categoryId = $("#modalEditCategory").data("category-id");
        const categoryName = $("#editCategoryName").val();
        const categoryDescription = $("#editCategoryDescription").val();

        console.log(`Category Name: ${categoryName}, Category Description: ${categoryDescription}, Category ID: ${categoryId}`);
        $.ajax({
            url: `/api/categories/${categoryId}`,
            method: "PUT",
            contentType: "application/json",
            data: JSON.stringify({
                name: categoryName,
                description: categoryDescription
            }),
            success: function (res) {
                console.log("Categoria atualizada:", res);
                loadCategories();
            },
            error: function (xhr) {
                console.error("Erro ao atualizar categoria:", xhr.responseText);
            }
        });

        $("#modalEditCategory").addClass("hidden");
    });

    $("#btnConfirmEditProduct").on("click", function (event) {
        event.preventDefault()

        const productId = $("#modalEditProduct").data("product-id");
        console.log("Product ID: ", productId)
        let newProductName = $("#editProductName").val();
        let newProductPrice = $("#editProductPrice").val();
        let newProductDescription = $("#editProductDescription").val();

        $.ajax({
            url: `/api/products/${productId}`,
            method: "PUT",
            contentType: "application/json",
            data: JSON.stringify({
                name: newProductName,
                description: newProductDescription,
                price: parseFloat(newProductPrice),
            }),
            success: function(res) {
                console.log("Produto atualizado com sucesso.");
                loadCategories();
                $("#editProductName").val("");
                $("#editProductPrice").val("");
                $("#editProductDescription").val("");
                $("#modalEditProduct").addClass("hidden");
            },
            error: function(xhr) {
                console.error("Erro ao atualizar produto:", xhr.responseText);
            }
        })
    })
});
