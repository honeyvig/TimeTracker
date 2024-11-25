import tkinter as tk
from tkinter import simpledialog
import time
import threading
import pyscreenshot as ImageGrab
from datetime import datetime
from PIL import Image, ImageTk

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker Application")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        self.start_time = None
        self.running = False
        self.latest_screenshot_path = None
        self.screenshot_interval = 5  # Screenshot capture interval in seconds

        # UI Colors
        self.bg_color = "#f9f9f9"
        self.text_color = "#333"
        self.primary_color = "#00a400"
        self.root.configure(bg=self.bg_color)

        # UI Setup
        self.create_header()
        self.create_toggle_button()
        self.create_screenshot_display()
        self.create_time_display()

    def create_header(self):
        """Create the task header."""
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=10)

        self.task_label = tk.Label(
            header_frame,
            text="Task: Not Started",
            font=("Arial", 14, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
        )
        self.task_label.pack(anchor="w", padx=15)

    def create_toggle_button(self):
        """Add a toggle button for starting and stopping the task."""
        self.toggle_button = tk.Button(
            self.root,
            text="Start Task",
            font=("Arial", 12),
            bg=self.primary_color,
            fg="white",
            command=self.toggle_task,
            height=2,
            width=20,
        )
        self.toggle_button.pack(pady=15)

    def create_screenshot_display(self):
        """Create the screenshot display section."""
        screenshot_frame = tk.Frame(self.root, bg=self.bg_color)
        screenshot_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        screenshot_label = tk.Label(
            screenshot_frame,
            text="Latest Screenshot:",
            font=("Arial", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
        )
        screenshot_label.pack(anchor="w", pady=5)

        self.screenshot_display = tk.Label(
            screenshot_frame,
            text="No screenshots yet",
            font=("Arial", 10),
            fg=self.primary_color,
            bg=self.bg_color,
            relief=tk.SOLID,
            bd=1,
            width=40,
            height=10,
            anchor="center",
        )
        self.screenshot_display.pack(fill=tk.BOTH, expand=True, pady=10)

    def create_time_display(self):
        """Create a section to display elapsed time."""
        self.time_display = tk.Label(
            self.root,
            text="Elapsed Time: 00:00:00",
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color,
        )
        self.time_display.pack(pady=10)

    def toggle_task(self):
        """Toggle between starting and stopping the task."""
        if self.running:
            self.stop_task()
        else:
            self.start_task()

    def start_task(self):
        """Start the task and begin screenshot capture."""
        self.start_time = time.time()
        self.running = True
        self.task_label.config(text="Task: Running")
        self.toggle_button.config(text="Stop Task", bg="red")

        # Start screenshot thread
        self.screenshot_thread = threading.Thread(target=self.capture_screenshots)
        self.screenshot_thread.start()

        # Update elapsed time
        self.update_time_display()

    def stop_task(self):
        """Stop the task."""
        self.running = False
        self.task_label.config(text="Task: Stopped")
        self.toggle_button.config(text="Start Task", bg=self.primary_color)

    def capture_screenshots(self):
        """Periodically capture screenshots."""
        while self.running:
            time.sleep(self.screenshot_interval)
            screenshot = ImageGrab.grab()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_{timestamp}.png"
            screenshot.save(screenshot_path)

            # Update UI with the latest screenshot
            self.latest_screenshot_path = screenshot_path
            self.display_screenshot(screenshot_path)

    def display_screenshot(self, screenshot_path):
        """Update the screenshot display with the latest capture."""
        try:
            img = Image.open(screenshot_path)
            img.thumbnail((300, 200))  # Resize for display
            screenshot_img = ImageTk.PhotoImage(img)
            self.screenshot_display.config(image=screenshot_img, text="")
            self.screenshot_display.image = screenshot_img  # Prevent garbage collection
        except Exception as e:
            print(f"Error loading screenshot: {e}")

    def update_time_display(self):
        """Update the elapsed time display."""
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            hours = elapsed_time // 3600
            minutes = (elapsed_time % 3600) // 60
            seconds = elapsed_time % 60
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.time_display.config(text=f"Elapsed Time: {time_str}")
            self.root.after(1000, self.update_time_display)


# Main Application Execution
root = tk.Tk()
app = TimeTrackerApp(root)
root.mainloop()
