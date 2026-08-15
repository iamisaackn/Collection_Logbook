# Aggregated reports
# reports.py – Management Aggregated Reports
import pandas as pd
from db import run_query


def calls_today() -> pd.DataFrame:
    sql = """
        SELECT
            u.full_name    AS officer_name,
            b.branch_name,
            COUNT(*)       AS total_calls,
            SUM(CASE WHEN ccn.call_outcome='PTP'  THEN 1 ELSE 0 END) AS ptp_count,
            SUM(CASE WHEN ccn.call_outcome='Paid' THEN 1 ELSE 0 END) AS paid_count
        FROM collection_case_note ccn
        JOIN "user" u ON u.user_id   = ccn.officer_id
        JOIN branch b ON b.branch_id = u.branch_id
        WHERE DATE(ccn.created_at) = CURRENT_DATE
        GROUP BY u.full_name, b.branch_name
        ORDER BY total_calls DESC;
    """
    return pd.DataFrame(run_query(sql))


def weekly_officer_productivity() -> pd.DataFrame:
    sql = """
        SELECT
            u.full_name                                    AS officer_name,
            COUNT(*)                                       AS total_notes,
            COUNT(DISTINCT ccn.loan_id)                   AS unique_customers,
            SUM(CASE WHEN call_outcome='PTP'  THEN 1 ELSE 0 END) AS ptp_secured,
            SUM(CASE WHEN call_outcome='Paid' THEN 1 ELSE 0 END) AS payments_confirmed,
            SUM(CASE WHEN status='Closed'     THEN 1 ELSE 0 END) AS cases_closed
        FROM collection_case_note ccn
        JOIN "user" u ON u.user_id = ccn.officer_id
        WHERE ccn.created_at >= DATE_TRUNC('week', CURRENT_DATE)
        GROUP BY u.full_name
        ORDER BY total_notes DESC;
    """
    return pd.DataFrame(run_query(sql))


def ptp_conversion_rate() -> pd.DataFrame:
    sql = """
        SELECT
            u.full_name AS officer_name,
            COUNT(CASE WHEN call_outcome='PTP'        THEN 1 END) AS ptp_made,
            COUNT(CASE WHEN call_outcome='Paid'       THEN 1 END) AS paid,
            COUNT(CASE WHEN call_outcome='Broken PTP' THEN 1 END) AS broken_ptp,
            ROUND(
                100.0 * COUNT(CASE WHEN call_outcome='Paid' THEN 1 END)
                      / NULLIF(COUNT(CASE WHEN call_outcome='PTP' THEN 1 END),0),
            1) AS conversion_rate_pct
        FROM collection_case_note ccn
        JOIN "user" u ON u.user_id = ccn.officer_id
        GROUP BY u.full_name
        ORDER BY conversion_rate_pct DESC NULLS LAST;
    """
    return pd.DataFrame(run_query(sql))
