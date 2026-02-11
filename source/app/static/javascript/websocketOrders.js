$(function () {
    const socket = io();
    const $ordersListDone = $("#orders-list-done");
    const $ordersListPending = $("#orders-list-accepts");
    const $ordersListCompleted = $("#orders-list-finish");
    const newOrderSound = new Audio("/static/sounds/notification-order-one.mp3");
    newOrderSound.volume = 1;

    const lists = {
        done: $ordersListDone,
        pending: $ordersListPending,
        completed: $ordersListCompleted,
        canceled: $ordersListCompleted,
    };

    const $loading = $(`
        <div id="loading-spinner" class="flex flex-col items-center justify-center py-10 text-gray-700">
            <div class="animate-spin rounded-full h-10 w-10 border-b-4 border-green-500 mb-3"></div>
            <span class="text-sm font-medium">Carregando pedidos...</span>
        </div>
    `);
    Object.values(lists).forEach($list => $list.html($loading.clone()));

    // Conexão com o WebSocket
    socket.on("connect", function () {
        console.log("Conectado ao WebSocket!");
        socket.emit("join_menu", { menu_id: menuId });
    });

    // Receber todos os pedidos iniciais
    socket.on("all_orders", function (data) {
        console.log("Pedidos existentes:", data.orders);
        renderOrders(data.orders);

        if (data.count_done_orders !== undefined) {
            $("#orders-count").text(data.count_done_orders);
        }
        if (data.count_pending_orders !== undefined) {
            $("#pending-count").text(data.count_pending_orders);
        }
        if (data.count_completed_orders !== undefined && data.count_canceled_orders !== undefined) {
            let total = (data.count_completed_orders + data.count_canceled_orders);
            $("#completed-count").text(total);
        }
    });

    // Atualização completa (novo pedido, exclusão etc.)
    socket.on("new_order", function (data) {
        console.log("Atualizando todos os pedidos:", data.orders);

        try {
            newOrderSound.currentTime = 0;
            newOrderSound.play();
        } catch (error) {
            console.warn("Som bloqueado até o usuário interagir com a página:", error);
        }

        renderOrders(data.orders);

        if (data.count_done_orders !== undefined) {
            $("#orders-count").text(data.count_done_orders);
        }
        if (data.count_pending_orders !== undefined) {
            $("#pending-count").text(data.count_pending_orders);
        }
        if (data.count_completed_orders !== undefined && data.count_canceled_orders !== undefined) {
            let total = (data.count_completed_orders + data.count_canceled_orders);
            $("#completed-count").text(total);
        }
    });

    // Atualização em tempo real de um pedido
    socket.on("order_status_update", function (data) {
        console.log("Pedido atualizado:", data.order);
        updateSingleOrder(data.order);

        if (data.count_done_orders !== undefined) {
            $("#orders-count").text(data.count_done_orders);
        }
        if (data.count_pending_orders !== undefined) {
            $("#pending-count").text(data.count_pending_orders);
        }
        if (data.count_completed_orders !== undefined && data.count_canceled_orders !== undefined) {
            let total = (data.count_completed_orders + data.count_canceled_orders);
            $("#completed-count").text(total);
        }
    });

    // Renderiza todas as listas
    function renderOrders(orders) {
        Object.values(lists).forEach($list => $list.empty());
        if (!orders || orders.length === 0) {
            Object.values(lists).forEach($list => {
                $list.html(`
                    <div class="text-center text-gray-600 py-6">
                        <p class="text-xl text-gray-900 font-bold">Nenhum pedido encontrado.</p>
                    </div>
                `);
            });
            return;
        }

        orders.forEach((order, index) => renderSingleOrder(order, index));
    }

    // Renderiza um pedido individual
    function renderSingleOrder(order, index) {
        const $targetList = lists[order.status] || $ordersListDone;
        const now = new Date(order.created_at).toLocaleTimeString("pt-BR", {
            timeZone: "America/Sao_Paulo",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        });

        // Botões dinâmicos
        let buttonsHTML = ""
        if (order.status === "done") {
        buttonsHTML = `
            <button class="text-xs font-semibold text-white bg-blue-500
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-details-order"
                title="Detalhes do pedido"
                data-id='${order.id}'>
                Detalhes
            </button>
            <button class="text-xs font-semibold text-white bg-red-600 hover:bg-red-700 
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-not-accept-order"
                data-id='${order.id}'
                title="Rejeitar pedido"
                >
                Rejeitar
            </button>
            <button class="text-xs font-semibold text-white bg-green-600 hover:bg-green-700 
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-accept-order"
                data-id='${order.id}'
                title="Aceitar pedido"
                >
                Aceitar
            </button>
        `;
        } else if (order.status === "pending") {
          buttonsHTML = `
            <button class="text-xs font-semibold text-white bg-blue-500
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 .btn-details-order btn-details-order"
                data-id='${order.id}'
                title="Detalhes do pedido"
                >
                Detalhes
            </button>
            <button class="text-xs font-semibold text-white bg-red-600 hover:bg-red-700 
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-cancel-order"
                data-id='${order.id}'
                title="Cancelar pedido"
                >
                Cancelar
            </button>
            <button class="text-xs font-semibold text-white bg-green-600 hover:bg-green-700 
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-conclude-order"
                data-id='${order.id}'
                title="Concluir pedido"
                >
                Concluir
            </button>
        `;
        } else if (order.status === "completed") {
              buttonsHTML = `
            <button class="text-xs font-semibold text-white bg-blue-500
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-details-order"
                title="Detalhes do pedido"
                data-id='${order.id}'>
                Detalhes
            </button>
        `;
        } else if (order.status === "canceled") {
              buttonsHTML = `
            <button class="text-xs font-semibold text-white bg-blue-500
                px-2.5 py-1 rounded-3xl shadow-sm transition-all duration-200 btn-details-order"
                data-id='${order.id}'
                title="Detalhes do pedido"
                >
                Detalhes
            </button>
        `;
        }

        function formatStatus(status) {
            switch (status) {
                case "done":
                    return `<span class="p-[2px] pl-[6px] pr-[6px] bg-emerald-300 text-emerald-900 rounded-3xl">Realizado</span>`;
                case "pending":
                    return `<span class="p-[2px] pl-[6px] pr-[6px] bg-amber-300 text-amber-900 rounded-3xl">Pendente</span>`;
                case "canceled":
                    return `<span class="p-[2px] pl-[6px] pr-[6px] bg-rose-300 text-rose-900 rounded-3xl">Cancelado</span>`;
                case "completed":
                    return `<span class="p-[2px] pl-[6px] pr-[6px] bg-indigo-300 text-indigo-900 rounded-3xl">Finalizado</span>`;
                default:
                    return `<span class="p-[2px] pl-[6px] pr-[6px] bg-gray-300 text-gray-800 rounded-3xl">${status}</span>`;
            }
        }
        const statusText = formatStatus(order.status);
        const $li = $(`
            <li class="p-3 mb-2 w-full rounded-xl shadow-sm border-2
                bg-white via-white transition-all duration-300"
                data-id="${order.id}">
                <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                        <h3 class="font-bold text-gray-800 text-lg tracking-tight">Pedido</h3>
                        <span class="font-bold text-gray-800 text-lg tracking-tight">#${order.order_number}</span>
                    </div>
                    <div>
                        ${buttonsHTML}
                    </div>
                </div>
                <hr class="border-t-1 border-gray-200 mb-2">
                <div class="space-y-0.5">
                    <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Status:</span> ${statusText} </p>
                    <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Nome:</span> ${order.name}</p>
                    <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Telefone:</span> ${order.telephone}</p>
                    <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Total:</span> R$ ${order.total_value.toFixed(2)}</p>
                    <p class="text-xs text-gray-600"><span class="font-semibold text-gray-800">Horário:</span> ${now}</p>
                </div>
                <hr class="border-t-1 border-gray-200 mb-2">
                <div class="flex">
                    <button class="bg-gray-200 hover:bg-gray-300 font-semibold text-gray-700 px-3 py-1 rounded-xl transition-colors w-1/2 h-full">Rejeitar pedido</button>
                    <button class="bg-[#111111] hover:bg-[#050505] text-white transition-colors font-semibold px-3 py-1 rounded-xl transition-all w-1/2">Aceitar pedido</button>
                </div>
            </li>
        `);
        $targetList.prepend($li.hide().slideDown(300));
    }

    // Atualiza um pedido específico (em tempo real)
    function updateSingleOrder(order) {
        // Remove o pedido anterior de todas as listas
        Object.values(lists).forEach($list => {
            $list.find(`[data-id='${order.id}']`).remove();
        });
        // Adiciona o pedido com o novo status
        renderSingleOrder(order, 0);
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
                data: JSON.stringify({ status: "canceled" }),
                success: function (res) {
                    console.log(`PUT /api/orders/${orderId}?menu_id=${menuId}`, res);
                    if (res.success) {
                        $modal.addClass("hidden");
                        const updatedOrder = res.data || { ...res.order, status: "canceled" };
                        updateSingleOrder(updatedOrder);
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

        $.ajax({
            url: `/api/orders/${orderId}/status?menu_id=${menuId}`,
            method: "PUT",
            contentType: "application/json",
            data: JSON.stringify({ status: "pending" }),
            success: function (res) {
                console.log(`PUT /api/orders/${orderId}?menu_id=${menuId}`, res);
                if (res.success) {
                    const updatedOrder = res.data || { ...res.order, status: "pending" };
                    updateSingleOrder(updatedOrder);
                } else {
                    alert("Erro ao atualizar pedido.");
                }
            },
            error: function (xhr) {
                console.error(`Erro na requisição PUT (${xhr.status}): ${xhr.responseText}`);
            },
        });
    });
    $ordersListPending.on("click", ".btn-conclude-order", function() {
        const orderId = $(this).data("id");
          $.ajax({
                url: `/api/orders/${orderId}/status?menu_id=${menuId}`,
                method: "PUT",
                contentType: "application/json",
                data: JSON.stringify({ status: "completed" }),
                success: function (res) {
                    console.log(`PUT /api/orders/${orderId}?menu_id=${menuId}`, res);
                    if (res.success) {
                        $modal.addClass("hidden");
                        const updatedOrder = res.data || { ...res.order, status: "canceled" };
                        updateSingleOrder(updatedOrder);
                    } else {
                        alert("Erro ao atualizar pedido.");
                    }
                },
                error: function (xhr) {
                    console.error(`Erro na requisição PUT (${xhr.status}): ${xhr.responseText}`);
                },
            });
    })
    $ordersListPending.on("click", ".btn-cancel-order", function () {
        const orderId = $(this).data("id");
        const $modal = $("#modalConfirmCancelOrder");
        const $btnConfirm = $("#btn-confirm-cancel-delete");
        $modal.removeClass("hidden");

        $btnConfirm.off("click").on("click", function () {
            $.ajax({
                url: `/api/orders/${orderId}/status?menu_id=${menuId}`,
                method: "PUT",
                contentType: "application/json",
                data: JSON.stringify({ status: "canceled" }),
                success: function (res) {
                    console.log(`PUT /api/orders/${orderId}?menu_id=${menuId}`, res);
                    if (res.success) {
                        $modal.addClass("hidden");
                        const updatedOrder = res.data || { ...res.order, status: "canceled" };
                        updateSingleOrder(updatedOrder);
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


    function getDetailsOrder() {
        const orderId = $(this).data("id");
        modalDetailsOrder.removeClass("hidden")
        console.log(`ID do Pedido: ${orderId}`)
        let URLGetProductsOrder = `/api/orders/${orderId}/products`
        $.ajax({
            url: URLGetProductsOrder,
            method: "GET",
            success: function (response) {
                let containerProductsInfo = $("#modalDetailsOrder_order_items");
                let containerProductsInfoTotal = $("#modalDetailsOrder_order_total")

                // Informações do Cliente
                let customerName = $("#modalDetailsOrder_client_name")
                let customerPhone = $("#modalDetailsOrder_client_phone")
                let customerAddress = $("#modalDetailsOrder_client_address")
                let customerHouseNumber = $("#modalDetailsOrder_client_number")

                let customerData = response.data.customer
                console.log(`Dados do cliente: ${customerData}`)
                customerName.text(customerData["name"])
                customerPhone.text(customerData["telephone"])
                customerAddress.text(customerData["address"])
                customerHouseNumber.text(customerData["house_number"])


                containerProductsInfo.html("");
                let totalPrice = response.data.total


                containerProductsInfoTotal.text(totalPrice)
                console.log("Produtos vindo do backend: ", response.data)
                response.data.items.forEach(item => {
                    containerProductsInfo.append(`
                    <li class="flex items-center gap-4 p-3 w-[330px] bg-white rounded-xl shadow-sm border transition">
                        <img 
                            src="${item.image_url}" 
                            alt="Imagem do produto ${item.name}"
                            class="w-16 h-16 object-cover rounded-lg border"
                            onerror="this.src='/static/images/no-image.png';"
                        />

                    <div class="flex flex-col">
                        <p class="text-base font-semibold text-gray-800 leading-none">
                             ${item.name}
                        </p>
                        <p class="text-sm text-gray-600">
                             R$ ${item.price.toFixed(2).replace('.', ',')}
                        </p>
                        <p class="text-sm text-gray-600">
                            Quantidade: ${item.quantity}
                        </p>
                    </div>
                    </li>
                    `);
                });

            },
            error: function (xhr) {
                console.error("➡ Status HTTP:", xhr.status);
                console.error("➡ Status Text:", xhr.statusText);
                try {
                    const json = xhr.responseJSON || JSON.parse(xhr.responseText);
                    console.error("➡ Resposta JSON do Backend:", json);
                } catch (_) {
                    console.warn("➡ Não foi possível converter responseText para JSON.");
                }
            }
        })
    }

    const modalDetailsOrder = $("#modalDetailsOrder")
    $ordersListDone.on("click", '.btn-details-order', getDetailsOrder)
    $ordersListPending.on("click", '.btn-details-order', getDetailsOrder)
    $ordersListCompleted.on("click", '.btn-details-order', getDetailsOrder)
});
























