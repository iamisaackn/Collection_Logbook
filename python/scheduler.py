# Auto follow-up scheduling
# scheduler.py – Automated Follow-up Scheduling & Reminders

from datetime import date, timedelta
from db import run_query, run_write


def auto_reschedule_no_answers(days_ahead: int = 1) -> int:
    """
    For all 'No Answer' notes with an overdue follow-up,
    push the follow-up date forward by days_ahead.
    Returns count of updated records.
    """
    sql = """
        UPDATE collection_case_note
        SET followup_date = CURRENT_DATE + %(days)s,
            updated_at    = NOW()
        WHERE call_outcome  = 'No Answer'
          AND followup_date < CURRENT_DATE
          AND status        = 'Open'
        RETURNING note_id;
    """
    result = run_query(sql, {"days": days_ahead})
    count = len(result)
    print(f"[✓] Auto-rescheduled {count} 'No Answer' follow-ups → +{days_ahead} day(s).")
    return count


def flag_broken_ptps() -> list[dict]:
    """
    Identify PTP notes where promise_date has passed but status is still Open.
    Updates call_outcome to 'Broken PTP'.
    Returns list of affected records.
    """
    sql = """
        UPDATE collection_case_note
        SET call_outcome = 'Broken PTP',
            updated_at   = NOW()
        WHERE call_outcome  = 'PTP'
          AND promise_date  < CURRENT_DATE
          AND status        = 'Open'
        RETURNING note_id, loan_id, officer_id, promise_date;
    """
    broken = run_query(sql)
    print(f"[✓] Flagged {len(broken)} broken PTP(s).")
    return broken


def run_morning_scheduler() -> None:
    """Run all automated scheduling tasks — call this at 07:00 daily."""
    print(f"\n Morning Scheduler — {date.today()}")
    print("-" * 40)
    auto_reschedule_no_answers(days_ahead=1)
    flag_broken_ptps()
    print("[✓] Scheduler complete.\n")


if __name__ == "__main__":
    run_morning_scheduler()
