import threading
import time
import schedule
from datetime import datetime
from tray import run_tray
from popup import show_popup
from tracker import init_excel

# Time slots to track: 5:00 AM to 2:00 AM (hours 5-23, 0, 1, 2)
TRACKED_HOURS = list(range(5, 24)) + [0, 1, 2]

def check_and_popup():
    now = datetime.now()
    if now.hour in TRACKED_HOURS and now.minute == 0:
        # Get the previous hour slot
        prev_hour = (now.hour - 1) % 24
        if prev_hour in TRACKED_HOURS:
            slot = f"{prev_hour:02d}:00 - {now.hour:02d}:00"
            show_popup(slot, now)

def run_scheduler():
    schedule.every().minute.do(check_and_popup)
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    # Initialize Excel on first run
    init_excel()

    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Run system tray (blocking - keeps app alive)
    run_tray()
