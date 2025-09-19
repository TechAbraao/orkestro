$(function () {
    const socket = io();
    const $ordersList = $("#orders-list");
    socket.on("new_order", function (data) {
        const $li = $("<li></li>")
            .text("Order ID: " + data.order_id)
            .addClass("p-3 border border-gray-200 rounded-md bg-green-50 text-gray-800");
        $ordersList.prepend($li);
    });
});
