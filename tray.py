import pystray
from PIL import Image, ImageDraw
import threading
import subprocess
import os
import sys

def create_icon_image():
    """Create a simple clock icon for the tray."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer circle
    draw.ellipse([4, 4, 60, 60], fill="#0F0F13", outline="#C8A96E", width=3)

    # Clock hands (showing 12 o'clock style)
    cx, cy = 32, 32
    # Hour hand
    draw.line([cx, cy, cx, cy - 14], fill="#C8A96E", width=3)
    # Minute hand
    draw.line([cx, cy, cx + 10, cy + 6], fill="#F0EDE8", width=2)
    # Center dot
    draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill="#C8A96E")

    return img

def open_excel():
    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hourly_tracker.xlsx")
    if os.path.exists(excel_path):
        if sys.platform == "win32":
            os.startfile(excel_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", excel_path])
        else:
            subprocess.Popen(["xdg-open", excel_path])

def test_popup():
    from popup import show_popup
    from datetime import datetime
    show_popup("Test: 09:00 - 10:00", datetime.now())

def run_tray():
    icon_image = create_icon_image()

    menu = pystray.Menu(
        pystray.MenuItem("⏱  Hourly Tracker — Running", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("📊 Open Excel Sheet", lambda icon, item: open_excel()),
        pystray.MenuItem("🧪 Test Popup Now", lambda icon, item: test_popup()),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("❌ Quit", lambda icon, item: icon.stop()),
    )

    icon = pystray.Icon(
        name="HourlyTracker",
        icon=icon_image,
        title="Hourly Tracker — Active",
        menu=menu
    )

    icon.run()
