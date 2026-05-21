def data_processing(data: list[dict]) -> dict[str, list[dict]]:
    """
    Function that takes a list of dictionaries and groups the records based on the existing categories.
    """
    grouped = {}
    for r in data:
        category = r["Categoria"]
        record = {k: v for k, v in r.items() if k != "Categoria"}
        grouped.setdefault(category, []).append(record)
    return grouped


def calculate_category_sales(data: dict[str, list[dict]]) -> dict[str, float]:
    """
    Function used to calculate total daily revenue for each category.
    """
    grouped_totals = {}
    for category, products in data.items():
        category_total_revenue = 0
        for product in products:
            quantity = int(product["Quantidade"])
            sale = float(product["Venda"])
            item_revenue = quantity * sale
            category_total_revenue += item_revenue
        grouped_totals[category] = round(category_total_revenue, 2)
    return grouped_totals


# Testing
if __name__ == "__main__":
    from pathlib import Path

    from extract import read_csv

    records = read_csv(Path("sales_pipeline/data/raw/sales_2025-11-10.csv"))
    grouped = data_processing(records)
    totals = calculate_category_sales(grouped)
    print(totals)
