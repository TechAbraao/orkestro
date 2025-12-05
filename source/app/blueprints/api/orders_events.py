from source.app.extesions.socket_io import socketio
from flask_socketio import emit, join_room
from source.app.settings.logging_settings import get_logger
from source.app.services import orders_services

logger = get_logger(__name__)

@socketio.on("join_menu")
def handle_join_menu(data):
    menu_id = data.get("menu_id")
    if not menu_id:
        emit("error", {"msg": "Menu ID não informado."})
        return

    join_room(menu_id)
    logger.info(f"Cliente entrou na sala do menu {menu_id}")

    orders = orders_services.get_order_by_menu_id(menu_id)
    count_done_orders = orders_services.count_orders_done(menu_id, status="done")
    count_pending_orders = orders_services.count_orders_done(menu_id, status="pending")
    count_completed_orders = orders_services.count_orders_done(menu_id, status="completed")
    count_canceled_orders = orders_services.count_orders_done(menu_id, status="canceled")

    emit("all_orders",
         {
        "menu_id": menu_id,
        "orders": orders,
        "count_done_orders": count_done_orders,
        "count_pending_orders": count_pending_orders,
        "count_completed_orders": count_completed_orders,
        "count_canceled_orders": count_canceled_orders
         })

def broadcast_order_update(menu_id, updated_order):
    count_done_orders = orders_services.count_orders_done(menu_id)
    count_pending_orders = orders_services.count_orders_done(menu_id, status="pending")
    count_completed_orders = orders_services.count_orders_done(menu_id, status="completed")
    count_canceled_orders = orders_services.count_orders_done(menu_id, status="canceled")


    socketio.emit(
        "order_status_update",
        {"menu_id": menu_id,
         "order": updated_order,
         "count_done_orders": count_done_orders,
         "count_pending_orders": count_pending_orders,
         "count_completed_orders": count_completed_orders,
         "count_canceled_orders": count_canceled_orders
         },
        room=menu_id
    )

