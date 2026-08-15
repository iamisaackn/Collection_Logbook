# collection_notes.py – Save & Update Collection Case Notes
from datetime import date, timedelta
from db import run_write, run_query


VALID_OUTCOMES = [
    "Answered", "No Answer", "Busy", "PTP",
    "Broken PTP", "Paid", "Refused to Pay",
    "Wrong Number", "Deceased",
]


def save_note(
    loan_id: int,
    officer_id: int,
    call_outcome: str,
    comments: str,
    promise_date: date = None,
    followup_date: date = None,
    status: str = "Open",
) -> int:
    """
    Insert a new collection case note.
    Auto-schedules follow-up date if not provided.
    Returns the new note_id.
    """
    if call_outcome not in VALID_OUTCOMES:
        raise ValueError(f"Invalid outcome: {call_outcome}. Choose from {VALID_OUTCOMES}")

    # Auto follow-up: default +1 day unless officer sets it
    if followup_date is None:
        followup_date = date.today() + timedelta(days=1)

    sql = """
        INSERT INTO collection_case_note
            (loan_id, officer_id, call_outcome, promise_date,
             followup_date, comments, status, created_at, updated_at)
        VALUES
            (%(loan_id)s, %(officer_id)s, %(call_outcome)s, %(promise_date)s,
             %(followup_date)s, %(comments)s, %(status)s, NOW(), NOW())
        RETURNING note_id;
    """
    params = {
        "loan_id":      loan_id,
        "officer_id":   officer_id,
        "call_outcome": call_outcome,
        "promise_date": promise_date,
        "followup_date": followup_date,
        "comments":     comments,
        "status":       status,
    }
    result = run_query(sql, params)
    note_id = result[0]["note_id"]
    print(f"[✓] Note saved — note_id={note_id}, follow-up={followup_date}")
    return note_id


def close_note(note_id: int) -> None:
    """Mark a note as Closed."""
    sql = """
        UPDATE collection_case_note
        SET status = 'Closed', updated_at = NOW()
        WHERE note_id = %(note_id)s;
    """
    run_write(sql, {"note_id": note_id})
    print(f"[✓] Note {note_id} closed.")


def get_notes_for_loan(loan_id: int) -> list[dict]:
    """Return all notes for a given loan, newest first."""
    sql = """
        SELECT ccn.*, u.full_name AS officer_name
        FROM collection_case_note ccn
        JOIN "user" u ON u.user_id = ccn.officer_id
        WHERE ccn.loan_id = %(loan_id)s
        ORDER BY ccn.created_at DESC;
    """
    return run_query(sql, {"loan_id": loan_id})
