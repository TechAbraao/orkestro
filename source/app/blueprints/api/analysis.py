from flask import render_template, request, abort, redirect, url_for, session, g, jsonify
from source.app.utils.decorators.authorizations import permissions
from source.app.services import stores_services, menu_services, orders_services, analysis_services
from source.app.settings.logging_settings import get_logger
from source.app.blueprints.routes import api
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

"""
    * Exibirá as vendas por semana, isto é:
    - Segunda-feira
    - Terça-feira
    - Quarta-feira
    - Quinta-feira
    - Sexta-feira
    - Sábado
    - Domingo
"""
@api.route("/analysis/sales-per-week", methods=["GET"])
@permissions(roles=["USER", "ADMIN"])
def api_sales_per_week():
    store_id = g.jwt_claims.get("sub")
    logger.info(f"[{dir_name}] Acessou o ambiente de análises da loja cujo 'store_id' = {store_id}")

    menu_id = menu_services.get_menu_id_by_store_id(store_id)
    logger.info(f"[{dir_name}] Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'")

    values, total_values = orders_services.get_sales_per_week(menu_id=menu_id)
    logger.info(f"[{dir_name}] Valores dos pedidos realizados na semana: {values}")
    logger.info(f"[{dir_name}] Valores totais dos pedidos realizados na semana: {str(total_values)}")

    total_values_float = [float(v) for v in total_values]

    return jsonify({
        "data": values,
        "total": total_values_float
    })

"""
    * Exibirá os seguintes status das vendas do Comércio:
    - Finalizado
    - Cancelado
    - Exibirá de forma geral? exibirá por semana? 
"""
@api.route("/analysis/status-per-week", methods=["GET"])
@permissions(roles=["USER", "ADMIN"])
def api_general_sales_status():
    store_id = g.jwt_claims.get("sub")
    logger.info(f"[Status por Semana] Acessou o ambiente de análises da loja cujo 'store_id' = {store_id}")

    menu_id = menu_services.get_menu_id_by_store_id(store_id)
    logger.info(f"Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'")

    cancel_count = orders_services.count_orders_done(menu_id=menu_id, status="canceled")
    completed_count = orders_services.count_orders_done(menu_id=menu_id, status="completed")
    logger.info(f"Através do 'menu_id' = '{menu_id}', obtém-se os seguintes status: Pedidos Cancelados: '{cancel_count}' - Pedidos Completos: '{completed_count}'")

    return jsonify({
        "data": [cancel_count, completed_count],
    })

"""
    * Exibirá a quantidade de pedidos totais realizadas no cardápio. 
"""
@api.route("/analysis/total-orders", methods=["GET"])
@permissions(roles=["USER", "ADMIN"])
def api_total_orders():
    store_id = g.jwt_claims.get("sub")
    logger.info(f"[Pedidos Totais] Acessou o ambiente de análises da loja cujo 'store_id' = {store_id}")

    menu_id = menu_services.get_menu_id_by_store_id(store_id)
    logger.info(f"Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'")

    value = analysis_services.number_or_orders_placed(menu_id)

    return jsonify({
        "data": value
    })

""" 
    * Exibirá a receita total diária. (24h)
"""
@api.route("/analysis/daily-recipe", methods=["GET"])
@permissions(roles=["USER", "ADMIN"])
def api_daily_recipe():
    store_id = g.jwt_claims.get("sub")
    logger.info(f"[Receita Total Diária] Acessou o ambiente de análises da loja cujo 'store_id' = {store_id}")

    menu_id = menu_services.get_menu_id_by_store_id(store_id)
    logger.info(f"Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'")

    total_value = analysis_services.total_sales_last_24h(menu_id)
    logger.info(f"Através do 'menu_id', a soma de TODOS os pedidos (nas últimas 24h) resultou em: R$ '{total_value}'")

    return jsonify({
        "data": total_value
    })