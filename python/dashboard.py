# Daily work queue
# dashboard.py – Daily Work Queue for Collection Officers

import pandas as pd
from db import run_query


def get_todays_followups(officer_id: int) -> pd.DataFrame:
    """Return today's follow-up queue for a given officer."""
    sql = """
        SELECT
            la.customer_name,
            la.loan_number,
            la.outstanding_balance,
            la.days_past_due,
            b.branch_name,
            lp.product_name,
            ccn.call_outcome  AS last_outcome,
            ccn.followup_date,
            ccn.comments
        FROM collection_case_note ccn
        JOIN loan_application la ON la.loan_id    = ccn.loan_id
        JOIN branch           b  ON b.branch_id   = la.branch_id
        JOIN loan_product     lp ON lp.product_id = la.product_id
        WHERE ccn.followup_date = CURRENT_DATE
          AND ccn.status        = 'Open'
          AND ccn.officer_id    = %(officer_id)s
        ORDER BY la.days_past_due DESC;
    """
    rows = run_query(sql, {"officer_id": officer_id})
    return pd.DataFrame(rows)


def get_ptp_due_today() -> pd.DataFrame:
    """Return all Promise-to-Pay cases due today."""
    sql = """
        SELECT
            la.customer_name,
            la.loan_number,
            la.outstanding_balance,
            ccn.promise_date,
            u.full_name AS officer_name
        FROM collection_case_note ccn
        JOIN loan_application la ON la.loan_id = ccn.loan_id
        JOIN "user"           u  ON u.user_id  = ccn.officer_id
        WHERE ccn.call_outcome = 'PTP'
          AND ccn.promise_date = CURRENT_DATE
          AND ccn.status       = 'Open'
        ORDER BY la.outstanding_balance DESC;
    """
    rows = run_query(sql)
    return pd.DataFrame(rows)


def get_overdue_followups() -> pd.DataFrame:
    """Return all overdue (missed) follow-ups."""
    sql = """
        SELECT
            la.customer_name,
            la.loan_number,
            ccn.followup_date,
            CURRENT_DATE - ccn.followup_date AS days_overdue,
            u.full_name AS officer_name
        FROM collection_case_note ccn
        JOIN loan_application la ON la.loan_id = ccn.loan_id
        JOIN "user"           u  ON u.user_id  = ccn.officer_id
        WHERE ccn.followup_date < CURRENT_DATE
          AND ccn.status        = 'Open'
        ORDER BY days_overdue DESC;
    """
    rows = run_query(sql)
    return pd.DataFrame(rows)


def print_dashboard(officer_id: int) -> None:
    """Pretty-print the daily dashboard to terminal."""
    print("\n" + "="*60)
    print(f" DAILY DASHBOARD — Officer ID: {officer_id}")
    print("="*60)

    sections = {
        "Today's Follow-ups": get_todays_followups(officer_id),
        "PTP Due Today": get_ptp_due_today(),
        "Overdue Follow-ups": get_overdue_followups(),
    }

    for title, df in sections.items():
        print(f"\n{title}  ({len(df)} records)")
        print("-"*60)
        print(df.to_string(index=False) if not df.empty else "  No records.")
