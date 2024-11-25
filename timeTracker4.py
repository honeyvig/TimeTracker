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
        self.root.geometry("800x600")

        self.start_time = None
        self.task_name = None
        self.screenshot_interval = 5  # Interval for screenshots in seconds
        self.running = False
        self.screenshots = []  # Store screenshot paths
        self.memos = []  # Store memos for the task
        self.chat_messages = []  # Store chat messages
        self.latest_screenshot_path = None

        # UI Elements
        self.create_toolbar()

        # Task Info Section
        self.task_info_frame = tk.Frame(root)
        self.task_info_frame.pack(pady=10)

        self.task_name_label = tk.Label(self.task_info_frame, text="Task Name: Not started", font=("Arial", 12))
        self.task_name_label.grid(row=0, column=0, padx=10, pady=5)

        self.memo_label = tk.Label(self.task_info_frame, text="Memo: None", font=("Arial", 12))
        self.memo_label.grid(row=1, column=0, padx=10, pady=5)

        self.screenshot_label = tk.Label(self.task_info_frame, text="Latest Screenshot: None", font=("Arial", 12))
        self.screenshot_label.grid(row=2, column=0, padx=10, pady=5)

        # Toggle Button
        self.toggle_button = tk.Button(root, text="Start Task", width=20, command=self.toggle_task)
        self.toggle_button.pack(pady=5)

        self.memo_button = tk.Button(root, text="Add Memo", width=20, command=self.add_memo)
        self.memo_button.pack(pady=5)

        # Chat Section
        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        self.chat_label = tk.Label(self.chat_frame, text="Chat Messages:", font=("Arial", 12))
        self.chat_label.pack(pady=5)

        self.chat_display = tk.Text(self.chat_frame, height=10, width=40)
        self.chat_display.pack(padx=10, pady=10)

        # Time Display
        self.time_display = tk.Label(root, text="Time: 00:00:00", font=("Arial", 12))
        self.time_display.pack(pady=10)

        self.screenshot_thread = None

        # Bottom Buttons
        self.create_bottom_buttons()

    def create_toolbar(self):
        """Create a custom toolbar with minimize and maximize buttons."""
        self.toolbar = tk.Frame(self.root, height=30, bg="gray")
        self.toolbar.pack(fill=tk.X)

        self.minimize_button = tk.Button(self.toolbar, text="_", width=3, command=self.minimize_window)
        self.minimize_button.pack(side=tk.LEFT)

        self.maximize_button = tk.Button(self.toolbar, text="☐", width=3, command=self.toggle_maximize)
        self.maximize_button.pack(side=tk.LEFT)

    def create_bottom_buttons(self):
        """Add Settings and Chat buttons at the bottom."""
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Settings Button
        settings_icon = ImageTk.PhotoImage(file="setting.png")  # Replace with your "setting.png" path
        settings_button = tk.Button(bottom_frame, image=settings_icon, command=self.task_settings, borderwidth=0)
        settings_button.image = settings_icon  # Prevent garbage collection
        settings_button.pack(side=tk.LEFT, padx=20)

        # Chat Button
        chat_icon = ImageTk.PhotoImage(file="message.png")  # Replace with your "message.png" path
        chat_button = tk.Button(bottom_frame, image=chat_icon, command=self.show_chat, borderwidth=0)
        chat_button.image = chat_icon  # Prevent garbage collection
        chat_button.pack(side=tk.RIGHT, padx=20)

    def minimize_window(self):
        """Minimize the window."""
        self.root.iconify()

    def toggle_maximize(self):
        """Toggle between maximize and restore."""
        current_state = self.root.state()
        if current_state == "normal":
            self.root.state('zoomed')
        else:
            self.root.state('normal')

    def toggle_task(self):
        """Toggle between starting and stopping the task."""
        if self.running:
            self.stop_task()
            self.toggle_button.config(text="Start Task")
        else:
            self.start_task()
            self.toggle_button.config(text="Stop Task")

    def start_task(self):
        """Start the task, track time, and take periodic screenshots."""
        self.start_time = time.time()
        self.running = True
        self.task_name = simpledialog.askstring("Input", "Enter task name:", parent=self.root)

        if self.task_name:
            self.task_name_label.config(text=f"Task Name: {self.task_name}")
            self.memo_label.config(text="Memo: None")

        self.screenshot_thread = threading.Thread(target=self.take_screenshots)
        self.screenshot_thread.start()

        self.update_time()

    def stop_task(self):
        """Stop the task and capture the final state."""
        self.running = False
        if self.screenshot_thread:
            self.screenshot_thread.join()

    def add_memo(self):
        """Allow the user to add a memo."""
        memo = simpledialog.askstring("Memo", "Enter your memo:", parent=self.root)
        if memo:
            self.memos.append(memo)
            self.memo_label.config(text=f"Memo: {memo}")

    def task_settings(self):
        """Allow the user to modify task settings."""
        new_task_name = simpledialog.askstring("Task Name", "Enter new task name:", parent=self.root)
        if new_task_name:
            self.task_name = new_task_name
            self.task_name_label.config(text=f"Task Name: {new_task_name}")

    def show_chat(self):
        """Display a chat dialog."""
        chat_message = simpledialog.askstring("Chat", "Enter your message:", parent=self.root)
        if chat_message:
            self.update_chat_messages(chat_message)

    def take_screenshots(self):
        """Periodically capture screenshots."""
        while self.running:
            time.sleep(self.screenshot_interval)
            screenshot = ImageGrab.grab()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_{timestamp}.png"
            screenshot.save(screenshot_path)

            # Update the latest screenshot path
            self.latest_screenshot_path = screenshot_path
            self.screenshots.append(screenshot_path)
            self.update_screenshot_display()

    def update_time(self):
        """Update the time display every second."""
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            hours = elapsed_time // 3600
            minutes = (elapsed_time % 3600) // 60
            seconds = elapsed_time % 60
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.time_display.config(text=f"Time: {time_str}")
            self.root.after(1000, self.update_time)

    def update_screenshot_display(self):
        """Update the screenshot display label."""
        if self.latest_screenshot_path:
            self.screenshot_label.config(text=f"Latest Screenshot: {self.latest_screenshot_path}")

    def update_chat_messages(self, message):
        """Update the chat messages display."""
        self.chat_messages.append(message)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.yview(tk.END)


# Create the main application window
root = tk.Tk()
app = TimeTrackerApp(root)

# Run the application
root.mainloop()
