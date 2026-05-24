from pathlib import Path

import pandas as pd
from decorators import log_stage


@log_stage
def save_totals(totals: dict[str, float], base_path: Path) -> tuple[Path, Path]:
    """
    Saves totals from transformation stage into .parquet and .csv files so it can be consumed downstream.
    """
    df = pd.DataFrame(totals.items(), columns=["Category", "Total_Revenue"])

    parquet_path = base_path.with_suffix(".parquet")
    csv_path = base_path.with_suffix(".csv")

    df.to_parquet(parquet_path)
    df.to_csv(csv_path, index=False)
    return parquet_path, csv_path
