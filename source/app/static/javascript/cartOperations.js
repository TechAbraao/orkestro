$(document).ready(function () {
    let cart = JSON.parse(window.localStorage.getItem('cartOrder') || "{}");

    if (!cart.products || cart.products.length === 0) {
        $("#cartItems").html(`
            <p class="text-gray-500 text-center">Seu carrinho está vazio.</p>
        `);
        $("#cartTotal").text("R$ 0,00");
        return;
    }

    function renderCart(cart) {
        const cartItems = $("#cartItems");
        cartItems.empty();
        let total = 0;

        cart.products.forEach(prod => {
            total += prod.price * prod.quantity;

            const itemHTML = `
                <div class="flex items-center justify-between w-[100%]
                bg-gray-50 p-4 rounded-xl border" data-id="${prod.product_id}">
                    
                    <div class="flex items-center gap-4">
                        
                        <img src="${prod.productImg}" class="w-[80px] h-[70px] rounded-lg bg-gray-200">

                        <div class="w-[250px]">
                            <h2 class="text-sm font-semibold">${prod.productName}</h2>

                            <p class="text-left text-sm font-semibold text-lg text-green-600 mt-1">
                                R$ ${(prod.price).toFixed(2)}
                            </p>

                            <button class="p-[2px] pl-[6px] pr-[6px] text-sm 
                                bg-rose-300 text-rose-900 rounded-3xl btn-delete">
                                Excluir
                            </button>
                        </div>

                        <div class="w-[150px] h-[70px] flex justify-center items-center flex-col">
                            <div class="flex items-center border rounded-lg w-[90px] justify-between px-2 py-1 mt-1">
                                <button class="minus-btn font-bold text-lg">−</button>
                                <span class="quantity text-sm">${prod.quantity}</span>
                                <button class="plus-btn font-bold text-lg">+</button>
                            </div>
                        </div>
                    </div>  
                </div>
            `;

            cartItems.append(itemHTML);
        });

        $("#cartTotal").text(`R$ ${total.toFixed(2)}`);
    }
    renderCart(cart);

    $(document).on("click", ".plus-btn", function () {
        const card = $(this).closest("[data-id]");
        const id = card.data("id");

        let item = cart.products.find(p => p.product_id === id);
        item.quantity++;

        window.localStorage.setItem("cartOrder", JSON.stringify(cart));
        renderCart(cart);
    });

    $(document).on("click", ".minus-btn", function () {
        const card = $(this).closest("[data-id]");
        const id = card.data("id");

        let item = cart.products.find(p => p.product_id === id);

        if (item.quantity > 1) {
            item.quantity--;
            window.localStorage.setItem("cartOrder", JSON.stringify(cart));
            renderCart(cart);
        }
    });

    $(document).on("click", ".btn-delete", function () {
        const card = $(this).closest("[data-id]");
        const id = card.data("id");

        cart.products = cart.products.filter(p => p.product_id !== id);

        window.localStorage.setItem("cartOrder", JSON.stringify(cart));
        renderCart(cart);
    });

    const modal = $("#modalFinishOrderId");
    const btnOpen = $(".btn-finish-order-cart");
    const closeBtn = modal.find(".close-modal");

    btnOpen.on("click", function () {
        modal.removeClass("hidden");
        setTimeout(() => {
            document.getElementById('modalCustomerName').focus();
        }, 50);
    });

    closeBtn.on("click", function () {
        modal.addClass("hidden");
    });

    modal.on("click", function (e) {
        if (e.target === this) {
            modal.addClass("hidden");
        }
    });

    const btnClearCart = $(".btn-clear-cart");
    btnClearCart.on("click", function () {
        const empty = {products: []};
        window.localStorage.removeItem("cartOrder");
        renderCart(empty);
    });
});
