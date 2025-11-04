$(function () {
    const socket = io();
    const $ordersList = $("#orders-list-new");
    console.log("MenuId", menuId);

    socket.on("connect", function () {
        console.log("Conectado ao WebSocket!");
        socket.emit("join_menu", { menu_id: menuId });
    });

    socket.on("all_orders", function (data) {
        console.log("Pedidos existentes:", data.orders);
        renderOrders(data.orders);
    });

    socket.on("new_order", function (data) {
        console.log("Novo pedido:", data.orders);
        renderOrders(data.orders);
    });

    function renderOrders(orders) {
        $ordersList.empty();
        orders.forEach((order, index) => {
            const now = new Date(order.created_at).toLocaleTimeString("pt-BR", {
                timeZone: "America/Sao_Paulo",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
            });

            const $li = $(`
                <li class="p-3 mb-2 w-full rounded-xl shadow-sm border-2 border-green-300 bg-gradient-to-br 
                    from-green-50 via-white to-green-100 transition-all duration-300">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-2">
                            <h3 class="font-bold text-gray-800 text-base tracking-tight">Pedido</h3>
                            <span class="font-bold text-gray-800 text-base tracking-tight">#${index + 1}</span>
                        </div>
                        <div>
                            <button class="text-xs font-semibold text-white bg-green-600 hover:bg-green-700 px-2.5 py-1 
                                rounded-3xl shadow-sm transition-all duration-200">
                                Detalhes
                            </button>
                            <button class="text-xs font-semibold text-white bg-green-600 hover:bg-green-700 px-2.5 py-1 
                                rounded-3xl shadow-sm transition-all duration-200">
                                Rejeitar
                            </button>
                            <button class="text-xs font-semibold text-white bg-green-600 hover:bg-green-700 px-2.5 py-1 
                                rounded-3xl shadow-sm transition-all duration-200">
                                Aceitar
                            </button>
                        </div>
                    </div>
                    <hr class="border-t-1 border-green-200 mb-2">
                    <div class="space-y-0.5">
                        <p class="text-xs text-gray-600">
                            <span class="font-semibold text-gray-800">Status:</span> ${order.status}
                        </p>
                        <p class="text-xs text-gray-600">
                            <span class="font-semibold text-gray-800">Nome:</span> ${order.name}
                        </p>
                        <p class="text-xs text-gray-600">
                            <span class="font-semibold text-gray-800">Telefone:</span> ${order.telephone}
                        </p>
                        <p class="text-xs text-gray-600">
                            <span class="font-semibold text-gray-800">Total:</span> R$ ${order.total_value}
                        </p>
                        <p class="text-xs text-gray-600">
                            <span class="font-semibold text-gray-800">Horário:</span> ${now}
                        </p>
                    </div>
                </li>
            `);
            $ordersList.prepend($li.hide().slideDown(300));
        });
    }
});
