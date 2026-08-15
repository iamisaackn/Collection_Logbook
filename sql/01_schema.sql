-- DB schema – new table only
-- EXISTING TABLES (READ-ONLY – shown for reference)
-- loan_application (loan_id, customer_name, loan_number, outstanding_balance, days_past_due, loan_status, branch_id, product_id, officer_id)
-- user (user_id, full_name, email, role, branch_id)
-- branch (branch_id, branch_name, region)
-- loan_product (product_id, product_name, interest_rate)
-- loan_payment (payment_id, loan_id, payment_date, amount_paid, payment_method)

-- NEW TABLE – collection_case_note
CREATE TABLE IF NOT EXISTS collection_case_note (
    note_id SERIAL PRIMARY KEY,
    loan_id INT NOT NULL,
    officer_id INT NOT NULL,
    call_outcome VARCHAR(50) NOT NULL,
    promise_date DATE,
    followup_date DATE NOT NULL,
    comments TEXT,
    status VARCHAR(10)  NOT NULL DEFAULT 'Open',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_loan FOREIGN KEY (loan_id) REFERENCES loan_application(loan_id),
    CONSTRAINT fk_officer FOREIGN KEY (officer_id) REFERENCES "user"(user_id),
    CONSTRAINT chk_status CHECK (status IN ('Open','Closed')),
    CONSTRAINT chk_outcome CHECK (call_outcome IN (
        'Answered','No Answer','Busy','PTP','Broken PTP',
        'Paid','Refused to Pay','Wrong Number','Deceased'))
);

CREATE INDEX IF NOT EXISTS idx_followup_date ON collection_case_note (followup_date, status);

CREATE INDEX IF NOT EXISTS idx_officer_created ON collection_case_note (officer_id, created_at);
