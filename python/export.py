# CSV export for MIS
# export.py – CSV Export for MIS Reporting
import os
from datetime import date
import pandas as pd
from reports import calls_today, weekly_officer_productivity, ptp_conversion_rate
from config import APP_CONFIG


def export_to_csv(df: pd.DataFrame, filename: str) -> str:
    """Save a DataFrame to the outputs/ folder and return the path."""
    os.makedirs(APP_CONFIG["export_dir"], exist_ok=True)
    filepath = os.path.join(APP_CONFIG["export_dir"], filename)
    df.to_csv(filepath, index=False)
    print(f"[✓] Exported → {filepath}  ({len(df)} rows)")
    return filepath


def run_daily_export() -> None:
    """Export all daily MIS reports to CSV."""
    today = date.today().strftime("%Y%m%d")

    export_to_csv(calls_today(), f"calls_today_{today}.csv")
    export_to_csv(weekly_officer_productivity(), f"officer_productivity_{today}.csv")
    export_to_csv(ptp_conversion_rate(), f"ptp_conversion_{today}.csv")

    print("\n[✓] Daily MIS export complete.")


if __name__ == "__main__":
    run_daily_export()