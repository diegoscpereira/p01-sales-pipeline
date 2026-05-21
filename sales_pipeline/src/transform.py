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

# Testing
if __name__ == "__main__":
    from pathlib import Path
    from extract import read_csv

    records = read_csv(Path("sales_pipeline/data/raw/sales_2025-11-10.csv"))
    grouped = data_processing(records)

    print(list(grouped.keys()))
    print(f"Total categories: {len(grouped)}")
    print(f"Records in 'Bebida': {len(grouped['Bebida'])}")
    print(f"First Bebida record: {grouped['Bebida'][0]}")