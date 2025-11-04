$(function () {
    const socket = io();
    const $ordersListDone = $("#orders-list-done");
    const $ordersListPending = $("#orders-list-accepts");
    const $ordersListCompleted = $("#orders-list-finish");

    const lists = {
        done: $ordersListDone,
        pending: $ordersListPending,
        completed: $ordersListCompleted,
    };

    console.log("MenuId", menuId);

    const $loading = $(`
        <div id="loading-spinner" class="flex flex-col items-center justify-center py-10 text-gray-700">
            <div class="animate-spin rounded-full h-10 w-10 border-b-4 border-green-500 mb-3"></div>
            <span class="text-sm font-medium">Carregando pedidos...</span>
        </div>
    `);
    Object.values(lists).forEach($list => $list.html($loading.clone()));


    // Conexão inicial
    socket.on("connect", function () {
        console.log("Conectado ao WebSocket!");
        socket.emit("join_menu", { menu_id: menuId });
    });

    // Receber lista inicial de pedidos
    socket.on("all_orders", function (data) {
        console.log("Pedidos existentes:", data.orders);
        renderOrders(data.orders);
    });

    // Atualização de pedidos (novo, editado, deletado)
    socket.on("new_order", function (data) {
        console.log("Atualizando TODOS os PEDIDOS:", data.orders);
        renderOrders(data.orders);
    });

    // de status de pedido (em tempo real)
    socket.on("order_status_update", function (data) {
        console.log("Pedido específico ATUALIZADO:", data.order);
        // updateSingleOrder(data.order);
    });


    // Renderização dos pedidos
    function renderOrders(orders) {
        $ordersListDone.empty();


        if (!orders || orders.length === 0) {
            $ordersListDone.html(`
                <div class="text-center text-gray-600 py-6">
                    <p class="text-xl text-gray-900 font-bold">Nenhum pedido encontrado.</p>
                </div>
            `);
            return;
        }


        orders.forEach((order, index) => {
            const now = new Date(order.created_at).toLocaleTimeString("pt-BR", {
                timeZone: "America/Sao_Paulo",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
            });

            const $li = $(`
                <li class="p-3 mb-2 w-full rounded-xl shadow-sm border-2 b
                    bg-gradient-to-br from-green-50 via-white to-green-100 transition-all duration-300">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-2">
                            <h3 class="font-bold text-gray-800 text-base tracking-tight">Pedido</h3>
                            <span class="font-bold text-gray-800 text-base tracking-tight">#${index + 1}</span>
                        </div>
                        <div>
                            <button class="text-xs font-semibold text-white bg-blue-500
                                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-details-order"
                                data-id='${order.id}'>
                                Detalhes
                            </button>
                            <button class="text-xs font-semibold text-white bg-red-600 hover:bg-red-700 
                                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-not-accept-order"
                                data-id='${order.id}'>
                                Rejeitar
                            </button>
                            <button class="text-xs font-semibold text-white bg-green-600 hover:bg-green-700 
                                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-accept-order"
                                data-id='${order.id}'>
                                Aceitar
                            </button>
                        </div>
                    </div>
                    <hr class="border-t-1 border-green-200 mb-2">
                    <div class="space-y-0.5">
                        <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Status:</span> ${order.status}</p>
                        <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Nome:</span> ${order.name}</p>
                        <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Telefone:</span> ${order.telephone}</p>
                        <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Total:</span> R$ ${order.total_value}</p>
                        <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Horário:</span> ${now}</p>
                    </div>
                </li>
            `);
            $ordersListDone.prepend($li.hide().slideDown(300));
        });
    }

    $ordersListDone.on("click", ".btn-not-accept-order", function () {
        const orderId = $(this).data("id");
        const $modal = $("#modalConfirmDeleteOrder");
        const $btnConfirm = $("#btn-confirm-order-delete");
        $modal.removeClass("hidden");

        $btnConfirm.off("click").on("click", function () {
            $.ajax({
                url: `/api/orders/${orderId}/status?menu_id=${menuId}`,
                method: "PUT",
                contentType: "application/json",
                data: JSON.stringify({
                    status: "canceled"
                }),
                success: function (res) {
                    console.log(`PUT /api/orders/${orderId}?menu_id=${menuId}`, res);
                    if (res.success) {
                        $modal.addClass("hidden");
                    } else {
                        alert("Erro ao atualizar pedido.");
                    }
                },
                error: function (xhr) {
                    console.error(`Erro na requisição PUT (${xhr.status}): ${xhr.responseText}`);
                },
            });
        });
    });
    $ordersListDone.on("click", ".btn-accept-order", function () {
        const orderId = $(this).data("id");
        console.warn("Hello, World!", orderId)
        $.ajax({
            url: `/api/orders/${orderId}/status?menu_id=${menuId}`,
            method: "PUT",
            contentType: "application/json",
            data: JSON.stringify({
                status: "pending"
            }),
            success: function (res) {
                console.log(`PUT /api/orders/${orderId}?menu_id=${menuId}`, res);
                if (res.success) {
                    $modal.addClass("hidden");
                } else {
                    alert("Erro ao atualizar pedido.");
                }
            },
            error: function (xhr) {
                console.error(`Erro na requisição PUT (${xhr.status}): ${xhr.responseText}`);
            },
        });
    })
});
