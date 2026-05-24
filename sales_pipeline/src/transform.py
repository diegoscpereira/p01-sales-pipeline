from loguru import logger
from validate import Sales


def data_processing(data: list[Sales]) -> dict[str, list[Sales]]:
    """
    Function that takes a list of dictionaries based on the Sales model and groups the records based on the existing categories.
    """
    grouped = {}
    for sale in data:
        category = sale.Categoria
        grouped.setdefault(category, []).append(sale)
    return grouped


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


# Testing
if __name__ == "__main__":
    from pathlib import Path
    from sys import stderr

    from extract import import_raw_csv_files
    from loguru import logger
    from validate import quarantine_records, validate_records

    logger.remove()

    logger.add(
        sink=stderr,
        format="{time:HH:mm:ss} | <level>{level: <8}</level> | {function} | {message}",
        level="INFO",
    )

    logger.add(sink="logs/pipeline.log", level="DEBUG", rotation="10 MB")

    logger.info("Pipeline started")

    records = import_raw_csv_files(Path("data/raw"))
    valid, invalid = validate_records(records)
    quarantine_records(invalid)
    grouped = data_processing(valid)
    totals = calculate_category_sales(grouped)
    logger.info(f"Pipeline finished. Totals: {totals}")  # ← and this
    print(totals)
