$(document).ready(function() {
    let storage = window.localStorage

    // Caso não existe 'cartOrder' e 'customerCredentials', o JavaScript redireciona para /menus/slug
    console.log(storage.getItem("customer"));
    if (storage.getItem("cartOrder") === null || storage.getItem("customerCredentials") == null) {
        window.location.href = `/menus/${menuSlug}`
    }

    const btnPlaceOrder = $(".btn-place-order")
    const modalOrderPlaced = $("#modalOrderPlaced")
    const btnFinishOrderPlaced = $(".btn-order-placed-finish")

    async function getUserIdByTelephone(telephone) {
        try {
            const res = await $.ajax({
                method: "GET",
                url: `/api/customers?telephone=${telephone}`,
            })
            return res.data.user_id
        } catch (error) {
            console.error("Erro ao buscar user_id:", error)
            return null
        }
    }

    async function getStoreId() {
        try {
            const res = await $.ajax({
                method: "GET",
                url: `/api/stores?slug=${menuSlug}`
            })
            return res.data
        } catch (error) {
            console.error("Erro ao buscar store_id:", error)
            return null
        }
    }

    async function finalizeOrderSend() {
        const user_id = await getUserIdByTelephone(customerCredentialsData.telephone)
        const store_id = await getStoreId()

        if (!user_id) {
            window.alert("Não foi possível obter o user_id. Pedido não efetuado.")
            return
        }

        let orderProducts = cartData.products
        const newCart = orderProducts.map(({ productImg, productName, price, ...rest }) => rest);

        const resStores = await fetch(`/api/stores/${menuSlug}/details`);
        const dataStores = await resStores.json();

        let order = {
            "menu_id": dataStores.data.id,
            "store_id": store_id.id,
            "user_id": user_id,
            "products": newCart
        }

        $.ajax({
            method: "POST",
            url: `/api/orders`,
            contentType: "application/json",
            data: JSON.stringify(order),
            success: function(res) {
                // Pedido realizado com sucesso. //
                modalOrderPlaced.removeClass("hidden")

                // Eliminar do LocalStorage as credenciais do cliente e o carrinho de compra. //
                storage.removeItem("cartOrder")
                storage.removeItem("customerCredentials")

                // Caso o usuário clique no botão do modal de pedido finalizado, será redirecionado ao //
                // cardápio onde realizou a compra imediatamente. //
                btnFinishOrderPlaced.on("click", function() {
                    window.location.href = `/menus/${menuSlug}`
                })

                // Redirecionamento (ao cardápio) após pedido ser concluído. //
                setTimeout(() => {
                    window.location.href = `/menus/${menuSlug}`
                    modalOrderPlaced.addClass("hidden")
                }, 11115000)
            },
            error: function (xhr, status, error) {
                console.group("❌ ERRO AJAX");

                console.log("Status HTTP:", xhr.status);
                console.log("Status Text:", xhr.statusText);

                console.log("Response Text:", xhr.responseText);
                console.log("Response JSON:", xhr.responseJSON);

                console.log("ReadyState:", xhr.readyState);
                console.log("jQuery Status:", status);
                console.log("Error Thrown:", error);
                console.log("Headers:", xhr.getAllResponseHeaders());

                console.groupEnd();
            }
        })
    }

    btnPlaceOrder.on("click", finalizeOrderSend)
})
