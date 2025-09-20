from source.app import create_app
from source.app.entities.stores_entity import StoresEntity
from source.app.settings.definitions_settings import db
from werkzeug.security import generate_password_hash
from flask import url_for

app = create_app()

stores_data = [
    {
        "name": "Loja Central",
        "email": "central@lojas.com",
        "password": "senha12345",
        "telephone": "+999999999"
    },
    {
        "name": "Loja Norte",
        "email": "norte@lojas.com",
        "password": "senha12345",
        "telephone": "+988888888"
    },
    {
        "name": "Loja Sul",
        "email": "sul@lojas.com",
        "password": "senha12345",
        "telephone": "+977777777"
    },
    {
        "name": "Loja Leste",
        "email": "leste@lojas.com",
        "password": "senha12345",
        "telephone": "+966666666"
    },
    {
        "name": "Loja Oeste",
        "email": "oeste@lojas.com",
        "password": "senha12345",
        "telephone": "+955555555"
    },
    {
        "name": "Loja VIP",
        "email": "vip@lojas.com",
        "password": "senha12345",
        "telephone": "+944444444"
    },
    {
        "name": "Loja Express",
        "email": "express@lojas.com",
        "password": "senha12345",
        "telephone": "+933333333"
    },
    {
        "name": "Loja Mega",
        "email": "mega@lojas.com",
        "password": "senha12345",
        "telephone": "+922222222"
    },
    {
        "name": "Loja Mini",
        "email": "mini@lojas.com",
        "password": "senha12345",
        "telephone": "+911111111"
    },
    {
        "name": "Loja Online",
        "email": "online@lojas.com",
        "password": "senha12345",
        "telephone": "+900000000"
    }
]

with app.app_context():
    for store in stores_data:
        new_store = StoresEntity(
            name=store["name"],
            email=store["email"],
            password=generate_password_hash(store["password"]),
            telephone=store["telephone"],
            logo_url='static/images/default-store-logo.png'
        )
        db.session.add(new_store)
    try:
        db.session.commit()
        db.session.close()
    except Exception as e:
        exit(f"Error populating the database: {e}")
    print("Store seeds inserted successfully.")
