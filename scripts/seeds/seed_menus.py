# scripts/seeds/seed_menus.py

from source.app import create_app
from source.app.entities.menus_entity import MenusEntity
from source.app.entities.stores_entity import StoresEntity
from source.app.settings.definitions_settings import db
from source.app.utils.slugs import *

app = create_app()

menus_data = [
    {
        "name": "Breakfast Menu",
        "description": "Delicious breakfast options including pancakes, eggs, and more."
    },
    {
        "name": "Lunch Menu",
        "description": "Tasty lunch meals including sandwiches, salads, and hot dishes."
    },
    {
        "name": "Dinner Menu",
        "description": "Evening meals with a variety of entrees and desserts."
    }
]

with app.app_context():
    stores = StoresEntity.query.all()
    for store in stores:
        for menu in menus_data:
            new_menu = MenusEntity(
                name=menu["name"],
                slug=slug_generator(menu["name"]),
                description=menu["description"],
                store_id=store.id
            )
            db.session.add(new_menu)
    try:
        db.session.commit()
    except Exception as e:
        exit(f"Error populating menus: {e}")
    print("Menu seeds inserted successfully!")
