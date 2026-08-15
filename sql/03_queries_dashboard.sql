-- 1. Today's Follow-up Queue (for a specific officer)
SELECT
    la.customer_name,
    la.loan_number,
    la.outstanding_balance,
    la.days_past_due,
    b.branch_name,
    lp.product_name,
    ccn.call_outcome        AS last_outcome,
    ccn.followup_date,
    ccn.comments
FROM collection_case_note ccn
JOIN loan_application la ON la.loan_id    = ccn.loan_id
JOIN branch           b  ON b.branch_id   = la.branch_id
JOIN loan_product     lp ON lp.product_id = la.product_id
WHERE ccn.followup_date = CURRENT_DATE
  AND ccn.status        = 'Open'
  AND ccn.officer_id    = :officer_id   -- bind param from Python
ORDER BY la.days_past_due DESC;

-- 2. Promise-to-Pay Cases Due Today
SELECT
    la.customer_name,
    la.loan_number,
    la.outstanding_balance,
    ccn.promise_date,
    u.full_name AS officer_name
FROM collection_case_note ccn
JOIN loan_application la ON la.loan_id  = ccn.loan_id
JOIN "user"           u  ON u.user_id   = ccn.officer_id
WHERE ccn.call_outcome  = 'PTP'
  AND ccn.promise_date  = CURRENT_DATE
  AND ccn.status        = 'Open'
ORDER BY la.outstanding_balance DESC;

-- 3. Overdue Follow-ups (missed follow-up dates)
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

-- 4. Customer Full Profile (officer opens a record)
SELECT
    la.customer_name,
    la.loan_number,
    la.outstanding_balance,
    la.days_past_due,
    la.loan_status,
    b.branch_name,
    lp.product_name,
    MAX(lp2.payment_date)  AS last_payment_date,
    MAX(lp2.amount_paid)   AS last_payment_amount
FROM loan_application la
JOIN branch       b   ON b.branch_id   = la.branch_id
JOIN loan_product lp  ON lp.product_id = la.product_id
LEFT JOIN loan_payment lp2 ON lp2.loan_id = la.loan_id
WHERE la.loan_id = :loan_id
GROUP BY la.loan_id, la.customer_name, la.loan_number,
         la.outstanding_balance, la.days_past_due,
         la.loan_status, b.branch_name, lp.product_name;
