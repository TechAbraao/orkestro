$(document).ready(() => {
    console.log(`Category ID in Products Page: ${categoryId}`)
    const productsSection = $("#productsSection")

    $.ajax({
        url: `/api/categories/${categoryId}/products`,
        method: "GET",
        success: function (response) {
            const products = response.data
            console.log("Resposta:", response)

            productsSection.empty()

            if (!products || products.length === 0) {
                productsSection.append(`
                    <p class="text-gray-500 text-center">Nenhum produto encontrado para esta categoria.</p>
                `)
                return
            }

            products.forEach(product => {
                let urlRedirect = `/menus/${menuSlug}/products/${product.id}`;
                const productCard = `
                    <div class="relative bg-white rounded-2xl p-6 w-[630px] 
                    h-[230px] border-2 border-gray-300 flex items-center text-center transform 
                    transition duration-300 product-item" data-id=${product.id}>
                        <div class="w-2/3 h-full flex items-center justify-center bg-gray-100 rounded-xl overflow-hidden border border-gray-200">
                            <img data-img="${product.image_url}" src="${product.image_url || '/static/images/default.png'}" alt="${product.name}" class="w-full h-full object-cover img-product-id">
                        </div>
                        <div class="w-full h-full">
                            <div class="w-full h-3/2">
                                <h3 data-name="${product.name}" class="text-[20px] font-semibold text-gray-800 mb-2 pl-3 pt-3 text-left name-product-id">${product.name}
                                </h3>
                                <p class="text-sm text-gray-500 line-clamp-2 pl-3 text-left">${product.description || "Sem descrição"}</p>
                                <p data-price="${product.price}" class="text-gray-800 font-medium mt-2 pl-3 text-left price-product-id">R$ ${product.price.toFixed(2)}</p>
                            </div>
                            {% if strategy["menu_roles"] == "COMMON" %}
                            <div class="w-full h-[42%] flex justify-end items-end">
                                <button class="bg-gray-800 p-2 rounded-2xl text-white text-sm font-semibold btn-add-cart-product">
                                    Adicionar no Carrinho
                                </button>
                            </div>
                            {% endif %}
                        </div>
                        <!-- Obter detalhes do Produto! -->
                       <!-- <a href="#" class="absolute inset-0 z-10"></a> -->
                    </div>
                `
                productsSection.append(productCard)
            })
        },
        error: function (xhr, status, error) {
            console.error("Erro ao carregar produtos da categoria")

            console.group("Detalhes do erro")
            console.log("Status HTTP:", xhr.status)
            console.log("Status text:", xhr.statusText)
            console.log("Response text:", xhr.responseText)
            console.log("Ready state:", xhr.readyState)
            console.log("Status da requisição:", status)
            console.log("Mensagem de erro do jQuery:", error)
            console.groupEnd()

            $("#productsSection").html(`
                <p class="text-red-500 text-center">Erro ao carregar produtos. Tente novamente mais tarde.</p>
            `)
        }
    })
    productsSection.on("click", ".btn-add-cart-product", function (e) {
        let productId = $(this).closest(".product-item").data("id");
        let productPrice = $(this).closest(".product-item").find(".price-product-id").data("price");
        let productImg = $(this).closest(".product-item").find(".img-product-id").data("img")
        let productName = $(this).closest(".product-item").find(".name-product-id").data("name")
        console.log(`ProductID: ${productId} - ProductPrice: ${productPrice} - ProductImg: ${productImg} - ProductName: ${productName}`)

        let cart = JSON.parse(window.localStorage.getItem("cartOrder")) || {
            menu_id: menuId,
            products: []
        };

        let existingProduct = cart.products.find(p => p.product_id === productId);
        if (existingProduct) {
            existingProduct.quantity += 1;
        } else {
            cart.products.push({
                product_id: productId,
                productImg: productImg,
                productName: productName,
                quantity: 1,
                price: productPrice
            });
        }
        window.localStorage.setItem("cartOrder", JSON.stringify(cart));
        console.log(`Produto ${productId} adicionado ao carrinho.`);
        console.log("Carrinho:", cart);
    });

    // Redirecionar para a aba de pagamentos / confirmar identidade
    const btnFinishOrder = $(".btn-finish-order")
    btnFinishOrder.on("click", function () {
        window.location.href = `/menus/${menuSlug}/cart`;
    });
})
