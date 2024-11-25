import tkinter as tk
from tkinter import simpledialog
import time
import threading
from datetime import datetime
from PIL import Image, ImageTk


class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker Application")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        self.start_time = None
        self.task_name = None
        self.running = False
        self.latest_screenshot_path = "No captures yet"

        # Styling Colors
        self.bg_color = "#f9f9f9"
        self.primary_color = "#00a400"
        self.text_color = "#333"
        self.border_color = "#ccc"

        self.root.configure(bg=self.bg_color)

        # Create UI Elements
        self.create_header()
        self.create_content_area()
        self.create_bottom_buttons()

    def create_header(self):
        """Create the header area with task details."""
        header_frame = tk.Frame(self.root, bg=self.bg_color, height=60)
        header_frame.pack(fill=tk.X, pady=10)

        self.task_name_label = tk.Label(
            header_frame,
            text="Refresh existing 3d-cart/shift...",
            font=("Arial", 14, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
        )
        self.task_name_label.pack(anchor="w", padx=15)

        self.subtext_label = tk.Label(
            header_frame,
            text="zachary rowe - zachary rowe",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color,
        )
        self.subtext_label.pack(anchor="w", padx=15)

    def create_content_area(self):
        """Create the main content area."""
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Current Session Time
        self.current_time_label = tk.Label(
            content_frame,
            text="0 hrs 0 m",
            font=("Arial", 24, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
        )
        self.current_time_label.pack(anchor="w", pady=10)

        self.current_session_label = tk.Label(
            content_frame,
            text="Current Session",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color,
        )
        self.current_session_label.pack(anchor="w")

        # Time Stats
        stats_frame = tk.Frame(content_frame, bg=self.bg_color)
        stats_frame.pack(fill=tk.X, pady=10)

        self.today_time_label = tk.Label(
            stats_frame,
            text="0:00 hrs Today (Mon UTC)",
            font=("Arial", 10),
            fg=self.primary_color,
            bg=self.bg_color,
        )
        self.today_time_label.pack(side=tk.LEFT, anchor="w")

        self.week_time_label = tk.Label(
            stats_frame,
            text="0:00 of 10 hrs This week (UTC)",
            font=("Arial", 10),
            fg=self.primary_color,
            bg=self.bg_color,
        )
        self.week_time_label.pack(side=tk.RIGHT, anchor="e")

        # Memo Section
        memo_frame = tk.Frame(content_frame, bg=self.bg_color, pady=10)
        memo_frame.pack(fill=tk.X)

        memo_label = tk.Label(
            memo_frame,
            text="Memo",
            font=("Arial", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
        )
        memo_label.pack(anchor="w", pady=5)

        self.memo_entry = tk.Entry(
            memo_frame,
            font=("Arial", 12),
            bg="white",
            fg=self.text_color,
            relief=tk.SOLID,
            bd=1,
        )
        self.memo_entry.pack(fill=tk.X)

        # Screenshot Section
        screenshot_frame = tk.Frame(content_frame, bg=self.bg_color, pady=10)
        screenshot_frame.pack(fill=tk.X)

        screenshot_label = tk.Label(
            screenshot_frame,
            text="Latest Screen Capture",
            font=("Arial", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
        )
        screenshot_label.pack(anchor="w", pady=5)

        screenshot_placeholder = tk.Label(
            screenshot_frame,
            text="No captures yet",
            font=("Arial", 10),
            fg=self.primary_color,
            bg=self.bg_color,
        )
        screenshot_placeholder.pack(fill=tk.BOTH, expand=True, pady=10)

        # View Work Diary
        work_diary_label = tk.Label(
            content_frame,
            text="View Work Diary",
            font=("Arial", 12, "underline"),
            fg=self.primary_color,
            bg=self.bg_color,
            cursor="hand2",
        )
        work_diary_label.pack(anchor="w", pady=5)

    def create_bottom_buttons(self):
        """Add settings and chat buttons at the bottom."""
        bottom_frame = tk.Frame(self.root, bg=self.bg_color, height=50)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Settings Button
        settings_icon = ImageTk.PhotoImage(file="setting.png")  # Replace with the path of "setting.png"
        settings_button = tk.Button(
            bottom_frame,
            image=settings_icon,
            command=self.task_settings,
            borderwidth=0,
            bg=self.bg_color,
        )
        settings_button.image = settings_icon  # Prevent garbage collection
        settings_button.pack(side=tk.LEFT, padx=20)

        # Chat Button
        chat_icon = ImageTk.PhotoImage(file="message.png")  # Replace with the path of "message.png"
        chat_button = tk.Button(
            bottom_frame,
            image=chat_icon,
            command=self.show_chat,
            borderwidth=0,
            bg=self.bg_color,
        )
        chat_button.image = chat_icon  # Prevent garbage collection
        chat_button.pack(side=tk.RIGHT, padx=20)

    def task_settings(self):
        """Display a task settings dialog."""
        new_task_name = simpledialog.askstring("Task Settings", "Enter new task name:", parent=self.root)
        if new_task_name:
            self.task_name_label.config(text=new_task_name)

    def show_chat(self):
        """Display a chat dialog."""
        chat_message = simpledialog.askstring("Chat", "Enter your message:", parent=self.root)
        if chat_message:
            print(f"Chat Message: {chat_message}")


# Run the application
root = tk.Tk()
app = TimeTrackerApp(root)
root.mainloop()
