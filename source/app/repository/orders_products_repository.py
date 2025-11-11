from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from source.app.entities.orders_products_entity import OrderProductsEntity
from source.app.entities.products_entity import ProductsEntity
from uuid import uuid4

class OrdersProductsRepository:
    def __init__(self):
        self.session = database.session

    @transactional
    def save_products_in_order(self, data):
        order_id = data.get("order_id")
        products = data.get("products", [])

        if not order_id:
            raise ValueError("order_id é obrigatório")
        if not products:
            raise ValueError("A lista de produtos não pode ser vazia")

        for item in products:
            product_id = item.get("product_id")
            quantity = item.get("quantity")

            if not product_id or not quantity:
                raise ValueError("product_id e quantity são obrigatórios")

            product_entity = (
                self.session.query(ProductsEntity)
                .filter(ProductsEntity.id == product_id)
                .first()
            )

            if not product_entity:
                raise ValueError(f"Produto '{product_id}' não encontrado")

            unit_price = product_entity.price

            entity = OrderProductsEntity(
                id=str(uuid4()),
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                price=unit_price
            )
            self.session.add(entity)

        return True

    def get_products_in_order(self, order_id):
        return self.session.query(OrderProductsEntity).filter(
            OrderProductsEntity.order_id == order_id
        ).all()

