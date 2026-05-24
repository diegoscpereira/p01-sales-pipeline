from decorators import log_stage
from loguru import logger
from validate import Sales


@log_stage
def data_processing(data: list[Sales]) -> dict[str, list[Sales]]:
    """
    Function that takes a list of dictionaries based on the Sales model and groups the records based on the existing categories.
    """
    grouped = {}
    for sale in data:
        category = sale.Categoria
        grouped.setdefault(category, []).append(sale)
    return grouped


@log_stage
def calculate_category_sales(data: dict[str, list[Sales]]) -> dict[str, float]:
    """
    Function used to calculate total daily revenue for each category within the Sales model.
    """
    grouped_totals = {}
    for category, products in data.items():
        category_total_revenue = 0
        for product in products:
            quantity = product.Quantidade
            sale = product.Venda
            item_revenue = quantity * sale
            category_total_revenue += item_revenue
        grouped_totals[category] = round(category_total_revenue, 2)
    logger.info(f"Category totals successfully calculated: {grouped_totals}")
    return grouped_totals
