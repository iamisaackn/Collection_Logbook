INSERT INTO branch (branch_id, branch_name, region) VALUES
  (1, 'Nairobi CBD',  'Nairobi'),
  (2, 'Westlands',    'Nairobi'),
  (3, 'Mombasa Road', 'Coast'),
  (4, 'Kisumu',       'Nyanza')
ON CONFLICT DO NOTHING;

INSERT INTO loan_product (product_id, product_name, interest_rate) VALUES
  (1, 'Logbook Loan',  18.0),
  (2, 'Business Loan', 24.0),
  (3, 'Personal Loan', 30.0)
ON CONFLICT DO NOTHING;

INSERT INTO "user" (user_id, full_name, email, role, branch_id) VALUES
  (1, 'Alice Mwangi', 'alice@presta.co.ke', 'Collection Officer', 1),
  (2, 'Brian Otieno', 'brian@presta.co.ke', 'Collection Officer', 2),
  (3, 'Carol Njeri',  'carol@presta.co.ke', 'Supervisor',         1)
ON CONFLICT DO NOTHING;

INSERT INTO loan_application
  (loan_id, customer_name, loan_number, outstanding_balance,
   days_past_due, loan_status, branch_id, product_id, officer_id)
VALUES
  (101, 'James Kamau',    'LN-2024-0101', 45000.00, 15, 'Active', 1, 1, 1),
  (102, 'Grace Wanjiku',  'LN-2024-0102', 12500.50, 32, 'Active', 1, 2, 1),
  (103, 'Peter Odhiambo', 'LN-2024-0103', 78000.00,  5, 'Active', 2, 1, 2),
  (104, 'Mary Achieng',   'LN-2024-0104',  5000.00, 60, 'Active', 3, 3, 2)
ON CONFLICT DO NOTHING;

INSERT INTO collection_case_note
  (loan_id, officer_id, call_outcome, promise_date, followup_date, comments, status)
VALUES
  (101, 1, 'PTP',       '2026-08-18', '2026-08-18', 'Customer promised KES 20,000 on Monday.', 'Open'),
  (102, 1, 'No Answer', NULL,         '2026-08-16', 'Called twice. No answer. Retry tomorrow.', 'Open'),
  (103, 2, 'Answered',  NULL,         '2026-08-20', 'Customer aware. Will visit branch.',       'Open'),
  (104, 2, 'Broken PTP','2026-08-14', '2026-08-15', 'Did not pay as promised. Escalate.',       'Open');
