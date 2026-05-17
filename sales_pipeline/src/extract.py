# Import pathlib for type hints
import csv
from pathlib import Path


# Functions
def read_csv(path: Path) -> list[dict]:
    """
    Function used to read the raw data, synced as .csv daily files. Stores data as a python list.
    """

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)
    return records


# Testing
if __name__ == "__main__":
    records = read_csv(Path("data/raw/sales_2025-11-10.csv"))
    print(records[0])
    print(len(records))
