$(function () {
    const socket = io();
    const $ordersList = $("#orders-list-new");

    let i = 0
    socket.on("new_order", function (data) {

        i++;
        const now = new Date().toLocaleTimeString("pt-BR", {
            timeZone: "America/Sao_Paulo",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        });
        const mockCustomer = {
            name: "Abraão Silva Santos",
            phone: "(11) 98765-4321",
            total: "300.00",
            count: i,
            hour: now
        };

        const $li = $(`
            <li class="p-3 mb-2 w-full rounded-xl shadow-sm border-2 border-green-300 bg-gradient-to-br 
                from-green-50 via-white to-green-100 transition-all duration-300">
                <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                        <h3 class="font-bold text-gray-800 text-base tracking-tight">Pedido</h3>
                        <span class="font-bold text-gray-800 text-base tracking-tight">#${mockCustomer.count}</span>
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
                <!--
                    <p class="text-sm text-gray-600">
                        <span class="font-semibold text-gray-800">ID:</span> ${data.order_id}
                    </p>
                -->
                    <p class="text-xs text-gray-600">
                        <span class="font-semibold text-gray-800">Cliente: ${mockCustomer.name}</span> 
                    </p>
                    <p class="text-xs text-gray-600">
                        <span class="font-semibold text-gray-800">Telefone: ${mockCustomer.phone}</span>
                    </p>
                    <p class="text-xs text-gray-600">
                        <span class="font-semibold text-gray-800">Total: R$ ${mockCustomer.total}</span>
                    </p>
                    <p class="text-xs text-gray-600">
                        <span class="font-semibold text-gray-800">Horário do Pedido: ${mockCustomer.hour}</span>
                    </p>
                </div>
            </li>
        `);

        $ordersList.prepend($li.hide().slideDown(300));
    });

    socket.on("welcome", function (data) {
        console.log(data);
    });
});
