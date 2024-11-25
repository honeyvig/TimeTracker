# TimeTracker
Features:

    Updated UI Layout:
        Toolbar with minimize/maximize buttons.
        Task title and a toggle button for starting/stopping tasks.

    Session Info:
        Displays session time and allows memo entry.
        Placeholder for the latest screenshot.

    Work Diary Button:
        A button to simulate additional features like opening a work diary.

This matches the structure and appearance of your uploaded screenshot. Let me know if further customization is needed!Features Added:

    Toggle Button:
        Starts or stops the task.
        Changes color and label based on the task state.

    Screenshot Capture:
        Periodically captures screenshots every 5 seconds when the task is running.
        Displays the latest screenshot dynamically in the UI.

    Time Display:
        Shows the elapsed time since the task started.
        Updates every second.

Steps to Test:

    Install pyscreenshot if not already installed:

pip install pyscreenshot

Run the script.
Click Start Task to begin and see the screenshot being displayed at regular intervals.
Stop the task by clicking the button again.
