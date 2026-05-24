import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    """
    Function used to read the raw data, synced as .csv daily files. Stores data as a python list.
    """

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)
    return records


def import_raw_csv_files(path: Path) -> list[dict]:
    """
    Function used to read all .csv from the source folder.
    It also aggregates the separate files into a single one.
    """
    all_records = []
    files = path.glob("*.csv")
    for file in files:
        file_date = file.stem.split("_")[1]
        records = read_csv(file)
        for record in records:
            record["Date"] = file_date
        all_records.extend(records)
    return all_records


# Testing
if __name__ == "__main__":
    func_test = import_raw_csv_files(Path("data/raw/"))
    print(f"Total records: {len(func_test)}")
    print(func_test[0])
    print(func_test[-1])
