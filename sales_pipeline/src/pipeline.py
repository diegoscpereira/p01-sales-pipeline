from pathlib import Path
from sys import stderr

from extract import import_raw_csv_files
from load import save_totals
from loguru import logger
from transform import calculate_category_sales, data_processing
from validate import log_stage, quarantine_records, validate_records


@log_stage
def run_pipeline(source: Path, output: Path) -> None:
    """
    Runs full ETL pipeline.
     1. Reads csvs in the raw layer ('bronze') - E
     2. Validates input and runs relevant transformations ('silver') - T
     3. Loads output file as .parquet and .csv ('gold') - L
    """
    records = import_raw_csv_files(source)
    valid, invalid = validate_records(records)
    quarantine_records(invalid)
    grouped = data_processing(valid)
    totals = calculate_category_sales(grouped)
    save_totals(totals, output)


def configure_logging() -> None:
    logger.remove()

    logger.add(
        sink=stderr,
        format="{time:HH:mm:ss} | <level>{level: <8}</level> | {function} | {message}",
        level="INFO",
    )

    logger.add(sink="logs/pipeline.log", level="DEBUG", rotation="10 MB")


# Testing
if __name__ == "__main__":
    configure_logging()
    run_pipeline(Path("data/raw"), Path("output/totals"))
