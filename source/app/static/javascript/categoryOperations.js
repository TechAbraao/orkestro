function copyProductId(id) {
    const input = document.createElement("input");
    input.value = id;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);

    console.log("ID copiado:", id);
}

const activatedColors = "bg-green-500 border-2 border-green-600"
const disabledColors = "bg-gray-300 border-2 border-gray-400"


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
        function copyText() {
            const text = document.getElementById("copyText").innerText;
            navigator.clipboard.writeText(text)
                .then(() => alert("Copiado!"))
                .catch(() => alert("Erro ao copiar"));
        }

        $.ajax({
            url: getCategoriesURL,
            method: "GET",
            success: function (res) {
                console.log("Todos os produtos: ", res);
                categoriesContainer.empty();

                if (res.success && res.data.length > 0) {
                    res.data.forEach(category => {
                        categoriesData = res.data;
                        const categoryCard = $(`
                            <div
                                class="bg-gradient-to-b from-white to-gray-50 rounded-2xl h-auto w-full p-6 border-4 border-gray-100
                                flex flex-col justify-between transform transition-all duration-300 border border-gray-100"
                            >
                                <div>
                                    <h3 class="text-3xl font-[#111111] font-semibold mb-5
                                     mb-2">
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
                                    ${ currentUserRoles.includes("ADMIN") || currentUserRoles.includes("PRIVILEGED") ? `
                                    <button
                                        class="delete-btn px-5 py-3 bg-red-500 text-base text-white rounded-3xl hover:bg-red-600 font-bold"
                                        data-id="${category.id}"
                                    >
                                        Excluir categoria
                                    </button> ` : `
                                    <button
                                        title="Permissão insuficiente"
                                        disabled
                                        class="px-5 py-3 rounded-full bg-gray-300 text-gray-500 text-sm font-semibold
                                        cursor-not-allowed opacity-70"
                                        data-id=""
                                    >
                                        Excluir categoria
                                    </button> 
                        
                                        `}
                                </div>
                                <div class="w-full bg-gray-200 h-[3px] mt-1 mb-4 rounded-full"></div>
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
                                        class="hidden bg-gray-50 mt-3 rounded-xl  p-4 space-y-3 
                                        border-2 border-gray-200 transition-all duration-300"
                                    >
                                        <section class="w-full grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                            ${(category.products || [])
                                                .map(
                                                    product => {
                                                        const isActive = product.activated
                                                        /*
                                                        console.log(`
                                                            ProductID: ${product.id},
                                                            Activated: ${product.activated}
                                                        `)
                                                        */
                                                        
                                                        const toggleBgClass = isActive ? `${activatedColors}` : `${disabledColors}`;
                                                        const toggleTranslateClass = isActive ? "translate-x-5" : "translate-x-0";
                                                        const ariaChecked = isActive ? "true" : "false";
                                                        
                                                        return `
                                                        <div class="flex justify-center gap-1 h-[285px] items-center bg-white rounded-lg px-4 
                                                        py-3 shadow-sm hover:shadow-md transition-all duration-200 border-2 border-gray-200 flex flex-col">
                                                            <div class="h-[35px] w-full flex justify-between items-center">
                                                                <p class="flex justify-center items-center gap-1">
                                                                  
                                                                        <img
                                                                            src="${copyIdIcon}"
                                                                            class="w-5 h-5 cursor-pointer"
                                                                            alt="Copy ID"
                                                                            title="Copiar ID"
                                                                         onclick="copyProductId('${product.id}')"
                                                                         >
                                                               
                                                                      <span
                                                                          class="cursor-pointer text-[14px] font-semibold"
                                                                          onclick="copyProductId('${product.id}')"
                                                                            title="${product.id}"
                                                                      >
                                                                         ${product.id.length > 13 ? product.id.slice(0, 13) + " ..." : product.id}
                                                                        </span>
                                                                    </p>
                                                                    <div>
                                                                    ${product.isPromotional  
                                                                        ? `<aside class="inline-flex items-center gap-1 px-3 py-1 text-xs font-semibold text-yellow-700 bg-yellow-100 rounded-full">
                                                                            <span class="w-2 h-2 bg-yellow-500 rounded-full"></span>
                                                                            Em promoção
                                                                        </aside>` 
                                                                        : ``
                                                                    }
                                                                   ${product.activated 
                                                                        ? `<aside class="inline-flex items-center gap-1 px-3 py-1 text-xs font-semibold text-green-700 bg-green-100 rounded-full">
                                                                            <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                                                                            Disponível
                                                                        </aside>` 
                                                                        : `<aside class="inline-flex items-center gap-1 px-3 py-1 text-xs font-semibold text-gray-600 bg-gray-100 rounded-full">
                                                                            <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
                                                                                Indisponível
                                                                           </aside>`
                                                                    }
                                                                    </div>
                                                            </div>
                                                            <div class="w-full bg-gray-200 h-[2px] mt-[2px] mb-[3px] rounded-full"></div>
                                                            <div class="w-full h-[60%] flex justify-between">
                                                                <div class="w-[50%] rounded-2xl h-full bg-green-100 overflow-hidden flex items-center justify-center">
                                                                    <img src="${product.image_url || ''}" alt="${product.name}" class="object-cover h-full w-full rounded-2xl">
                                                                </div>
                                                                <div class="w-full p-2">
                                                                    <span class="text-gray-800 font-medium text-lg block">${product.name}</span>
                                                                    ${
                                                                       product.isPromotional ? `
                                                                            <div class="flex flex-col">
                                                                                <span class="text-xs text-gray-400 line-through">
                                                                                    R$ ${Number(product.price ?? 0).toFixed(2)}
                                                                                </span>
                                                                                <span class="text-sm font-semibold text-green-600">
                                                                                    R$ ${Number(product.price_promotional ?? 0).toFixed(2)}
                                                                                </span>
                                                                            </div>
                                                                                    ` : `
                                                                            <span class="text-sm text-gray-500 block">
                                                                                R$ ${Number(product.price ?? 0).toFixed(2)}
                                                                            </span>
                                                                        `
                                                                    }
                                                                    <span 
                                                                    class="text-sm text-gray-500 w-[240px] break-words block"
                                                                    title="${product.description}"
                                                                    >${product.description.length > 35 ? product.description.slice(0, 35) + " ..." : product.description}</span>
                                                                </div>
                                                            </div>
                                                            <div class="w-full bg-gray-200 h-[2px] mt-1 rounded-full"></div>
                                                            <div class="flex justify-between gap-1 mt-1 w-full h-[65px]">
                                                                <button id="btn-edit-product" data-id="${product.id}"
                                                                        class="bg-gray-200 hover:bg-gray-300 font-semibold text-gray-700 
                                                                        px-3 py-1 rounded-xl transition-colors w-full h-[55px]">
                                                                        Configurações
                                                                </button>
                                                                <button id="btn-delete-product" data-id="${product.id}"
                                                                        class="bg-[#111111] hover:bg-[#050505] text-white transition-colors 
                                                                        font-semibold px-3 py-1 rounded-xl transition-all w-full h-[55px]">
                                                                        Excluir
                                                                </button>
                                                            </div>
                                                        </div>
                                                    `
                                                    }
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
    console.warn("PREÇO DA PROMO^ÇÂO PORA:" + JSON.stringify(selectedProduct));
    $("#editProductPricePromotional").val(selectedProduct.price_promotional);
    modalEditProduct.data("product-id", productId);


    const $toggleStatus = modalEditProduct.find(".productToggleStatus");
    const isActive = selectedProduct.activated;
    console.log("STATUS" + isActive)

    $toggleStatus.data("id", productId);
    $toggleStatus.attr("aria-checked", isActive.toString());

    $toggleStatus
        .removeClass(`${activatedColors} ${disabledColors}`)
        .addClass(isActive ? activatedColors : disabledColors);

    $toggleStatus.find("span")
        .removeClass("translate-x-5 translate-x-0")
        .addClass(isActive ? "translate-x-5" : "translate-x-0");


    const $togglePromo = modalEditProduct.find(".productTogglePromo");
    const isActivePromo = selectedProduct.isPromotional;
    console.log("PROMO:" + isActivePromo)

    $togglePromo.attr("aria-checked", isActivePromo.toString());
    $togglePromo
        .removeClass(`${activatedColors} ${disabledColors}`)
        .addClass(isActivePromo ? activatedColors : disabledColors);

    $togglePromo.find("span")
        .removeClass("translate-x-5 translate-x-0")
        .addClass(isActivePromo ? "translate-x-5" : "translate-x-0");
    
    const $inputPromo = $("#editProductPricePromotional");
    if (isActivePromo) {
        $inputPromo.prop("disabled", false);
        $inputPromo.focus();
    } else {
        $inputPromo.prop("disabled", true);
        $inputPromo.val(""); 
    }
    
    modalEditProduct.removeClass("hidden");
    $("#editProductName").focus();
});



$(document).on("click", ".productToggleStatus", function () {
    const $button = $(this);
    const isActive = $button.attr("aria-checked") === "true";
    const newState = !isActive;

    $button.attr("aria-checked", newState.toString());

    $button
        .removeClass(`${activatedColors} ${disabledColors}`)
        .addClass(newState ? activatedColors : disabledColors);

    $button.find("span")
        .removeClass("translate-x-5 translate-x-0")
        .addClass(newState ? "translate-x-5" : "translate-x-0");

});


$(document).on("click", ".productTogglePromo", function () {
    const $button = $(this);
    const isActive = $button.attr("aria-checked") === "true";
    const newState = !isActive;
    
    $button.attr("aria-checked", newState.toString());
    
    $button
    .removeClass(`${activatedColors} ${disabledColors}`)
    .addClass(newState ? activatedColors : disabledColors);
    
    $button.find("span")
    .removeClass("translate-x-5 translate-x-0")
    .addClass(newState ? "translate-x-5" : "translate-x-0");
    
    const $inputPromo = $("#editProductPricePromotional");
    if (newState) {
        $inputPromo.prop("disabled", false);
        $inputPromo.focus();
    } else {
        $inputPromo.prop("disabled", true);
        $inputPromo.val(""); 
    }
});



$("#btnConfirmEditProduct").on("click", function (event) {
    event.preventDefault();

    const productId = $("#modalEditProduct").data("product-id");
    const newProductName = $("#editProductName").val();
    const newProductPrice = $("#editProductPrice").val();
    const newProductDescription = $("#editProductDescription").val();
    const newInputPromo = $("#editProductPricePromotional").val();

    const toggleState = $("#modalEditProduct")
        .find(".productToggleStatus")
        .attr("aria-checked") === "true";

    const togglePromo = $("#modalEditProduct")
        .find(".productTogglePromo")
        .attr("aria-checked") === "true"    

    $.ajax({
        url: `/api/products/${productId}`,
        method: "PATCH",
        contentType: "application/json",
        data: JSON.stringify({
            name: newProductName,
            description: newProductDescription,
            price: parseFloat(newProductPrice),
            isPromotional: togglePromo,
            price_promotional: parseFloat(newInputPromo),
        }),
        success: function () {
            console.warn("Produto atualizado com sucesso.");
            $.ajax({
                url: `/api/products/${productId}/status`,
                method: "PATCH",
                contentType: "application/json",
                data: JSON.stringify({ activated: toggleState }),
                success: function () {
                    console.warn("Status do produto atualizado com sucesso:", toggleState);
                    console.warn("isPromotion do Produto: ", togglePromo)
                    loadCategories();
                    $("#editProductName").val("");
                    $("#editProductPrice").val("");
                    $("#editProductDescription").val("");
                    $("#modalEditProduct").addClass("hidden");
                },
                error: function (xhr) {
                    console.error("Erro ao atualizar status:", xhr.responseText);
                }
            });

        },
        error: function (xhr) {
            console.error("Erro ao atualizar produto:", xhr.responseText);
        }
    });
});
});
