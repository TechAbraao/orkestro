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
                            <img src="${product.image_url || '/static/images/default.png'}" alt="${product.name}" class="w-full h-full object-cover">
                        </div>
                        <div class="w-full h-full">
                            <div class="w-full h-3/2">
                                <h3 class="text-2xl font-semibold text-gray-800 mb-2 pl-3 pt-3 text-left">${product.name}</h3>
                                <p class="text-sm text-gray-500 line-clamp-2 pl-3 text-left">${product.description || "Sem descrição"}</p>
                                <p data-price="${product.price}" class="text-gray-800 font-medium mt-2 pl-3 text-left price-product-id">R$ ${product.price.toFixed(2)}</p>
                            </div>
                            <div class="w-full h-[42%] flex justify-end items-end">
                                <button class="bg-gray-800 p-2 rounded-2xl text-white text-sm font-semibold btn-add-cart-product">
                                    Adicionar no Carrinho
                                </button>
                            </div>
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
    // Estrutura pra salvar no LocalStorage
         /*
            "menu_id": ...,
            "user_id": ...,
            "products": [
            {
            "product_id": "19b8fe8f-50c7-4d9e-a8c0-c3c97a4c3de9",
            "quantity": 2
            },
            {
            "product_id": "e49e8568-442e-4cac-8aea-c810f5c47724",
            "quantity": 2
            },
         */
    productsSection.on("click", ".btn-add-cart-product", function (e) {

        let productId = $(this).closest(".product-item").data("id");

        let productPrice = $(this)
            .closest(".product-item")
            .find(".price-product-id")
            .data("price");

        console.log("menu_id:", menuId);


        let cart = JSON.parse(window.localStorage.getItem("cartOrder")) || {
            menu_id: menuId,
            user_id: "N/A",
            products: []
        };

        let existingProduct = cart.products.find(p => p.product_id === productId);
        if (existingProduct) {

            existingProduct.quantity += 1;
        } else {
            cart.products.push({
                product_id: productId,
                quantity: 1,
                price: productPrice
            });
        }
        window.localStorage.setItem("cartOrder", JSON.stringify(cart));
        console.log(`Produto ${productId} adicionado ao carrinho.`);
        console.log("Carrinho:", cart);
    });

    const btnClearCart = $(".btn-clear-cart")
    btnClearCart.on("click", function () {
        window.localStorage.removeItem("cartOrder");
    })
    // Redirecionar para a aba de pagamentos / confirmar identidade
    const btnFinishOrder = $(".btn-finish-order")
    btnFinishOrder.on("click", function () {

        // IMPORTANTE - tem que pegar o ATUAL momento do carrinho
        // Se não tiver nada, retorna para trás
        let cartNow = localStorage.getItem("cartOrder");
        if (!cartNow) {
            window.location.href = `/menus/${menuSlug}`;
            return;
        }
        const payload = {
            cart: JSON.parse(cartNow),
            category_id: categoryId
        };
        fetch("/api/cart/validate-cart", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        })
            .then(r => {
                if (r.status === 400) {
                    window.location.href = `/menus/${menuSlug}`;
                } else {
                    window.location.href = `/menus/${menuSlug}/cart`;
                }
            })
            .catch(err => {
                console.error("Erro no fetch:", err);
                window.location.href = `/menus/${menuSlug}`;
            });
    });
})
