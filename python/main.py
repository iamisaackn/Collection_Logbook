# Entry point
# main.py – Application Entry Point
from scheduler import run_morning_scheduler
from dashboard import print_dashboard
from export import run_daily_export


def main():
    print("Collection Logbook Automation")

    # 1. Run morning automation (broken PTPs, reschedule no-answers)
    run_morning_scheduler()

    # 2. Show dashboard for officer ID 1 (replace with session user)
    print_dashboard(officer_id=1)

    # 3. Export MIS reports to CSV
    run_daily_export()


if __name__ == "__main__":
    main()
