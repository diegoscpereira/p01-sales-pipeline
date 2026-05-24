import csv
from datetime import datetime
from pathlib import Path

from loguru import logger
from pydantic import BaseModel, Field, ValidationError


class Sales(BaseModel):
    Produto: str = Field(min_length=1)
    Categoria: str = Field(min_length=1)
    Quantidade: int = Field(ge=0)
    Venda: float = Field(gt=0)
    Date: str = Field(min_length=1)


def validate_records(records: list[dict]) -> tuple[list[Sales], list[dict]]:
    """
    Function used to run Pydantic validation tests after reading the raw .csv files from raw.
    Works as the validation gate before actually grouping the records and running the full pipeline.
    If any record is invalid, it will save it in quarentine. Proceeds to the transformation step otherwise.
    """
    valid = []
    invalid = []
    for record in records:
        try:
            sales_data = Sales(**record)  # ← Pydantic validates here
            valid.append(sales_data)
        except ValidationError as e:
            invalid.append(record)  # keep the original dict for quarantine
            reasons = "; ".join(
                f"{err['loc'][0]}={err['input']!r} ({err['msg']})" for err in e.errors()
            )
            logger.warning(f"Invalid record: {reasons}")
    total_records = len(valid) + len(invalid)
    logger.info(
        f"{total_records} records assessed: {len(valid)} valid | {len(invalid)} invalid."
    )
    return valid, invalid


def quarantine_records(records: list[dict]) -> Path | None:
    """
    Saves invalid records from the `validate_records` function into a quarantine csv file.
    """

    field_names = [
        "Produto",
        "Categoria",
        "Quantidade",
        "Venda",
        "Date",
        "Datetime_Quarantined",
    ]

    if not records:
        return None

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records_to_write = [{**record, "Datetime_Quarantined": now} for record in records]

    path = Path("output/quarantine/quarantine.csv")
    write_header_check = not path.exists()

    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        if write_header_check:
            writer.writeheader()
        writer.writerows(records_to_write)
    logger.warning(f"{len(records_to_write)} quarantined and saved to {path}")
    return path


# Testing
if __name__ == "__main__":
    from pathlib import Path

    from extract import import_raw_csv_files

    records = import_raw_csv_files(Path("data/raw"))
    valid, invalid = validate_records(records)
    quarantine_records(invalid)
    print(f"Quarantined {len(invalid)} rows")
