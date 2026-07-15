# Collection Logbook Automation (MVP)

The application sits **alongside the existing loan system**. It doesn't replace it.

Instead, it helps collection officers record customer interactions in a structured way and automatically organize their daily work.

## Step 1: Display Existing Loan Information

The application reads customer information from the existing database.

It mainly uses:

* `loan_application` – Loan details (customer, balance, loan status, loan number)
* `user` – Collection officer information
* `branch` – Branch details
* `loan_product` – Loan product
* `loan_payment` – Latest payment information (optional)

No data is changed in these tables—they are only read.

---

## Step 2: Officer Opens a Customer

Instead of searching through Excel or writing notes in Notepad, the officer opens a customer record.

The application automatically displays:

* Customer Name
* Loan Number
* Outstanding Balance
* Days Past Due
* Branch
* Product
* Last Payment

---

## Step 3: Officer Completes a Form

After calling the customer, the officer fills in a simple form.

Example:

* Call Outcome
* Promise to Pay Date
* Follow-up Date
* Comments
* Status (Open / Closed)

This takes less than a minute.

---

## Step 4: Save the Collection Note

When the officer clicks **Save**, the system automatically:

* Records the current date and time
* Records which officer created the note
* Links the note to the correct loan
* Schedules the next follow-up
* Makes the note available to supervisors

This information is stored in **one new table**, for example:

`collection_case_note`

This keeps the existing loan database unchanged.

---

## Step 5: Daily Dashboard

When officers log in the next morning, the application automatically shows:

* Customers to call today
* Promise-to-Pay cases due today
* Overdue follow-ups
* Completed follow-ups

The officer no longer needs reminders in Excel or sticky notes.

---

## Step 6: Management Reports

Managers can instantly view:

* Calls made today
* Calls by officer
* Calls by branch
* Promise-to-Pay cases
* Overdue follow-ups

They can also export the information to CSV for MIS reporting.

---

# Technology Roles

**SQL**

* Reads loan information from the existing database.
* Stores collection notes.
* Produces reports.

**Python**

* Automates repetitive tasks such as timestamps, follow-up scheduling, dashboard updates, reminders, and CSV exports.

**R**

* Creates weekly and monthly management reports with charts showing collection performance, officer productivity, and follow-up trends.

---

## Database Tables Used

| Purpose                           | Table                  |
| --------------------------------- | ---------------------- |
| Loan information                  | `loan_application`    |
| Collection officer                | `user`               |
| Branch                            | `branch`             |
| Loan product                      | `loan_product`       |
| Payment history (optional)        | `loan_payment`       |
| **New table for the application** | `collection_case_note` |
