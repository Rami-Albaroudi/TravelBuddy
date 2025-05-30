"""
Main module for the Travel Agent Record Management System GUI.
This module defines the main application window and manages the integration
of client, airline, and flight management interfaces.
"""

# Imports
import tkinter as tk
from tkinter import ttk, messagebox
from data.record_manager import RecordManager
from .client_gui import ClientGUI
from .flight_gui import FlightGUI
from .airline_gui import AirlineGUI


class TravelAgentApp(tk.Tk):
    """
    Main application class for the Travel Agent Record Management System.
    This class sets up the main window, manages navigation between different
    record types, and coordinates the overall application flow.
    """

    def __init__(self):
        super().__init__()

        # Configure main window
        self.title("Travel Agent Record Management System")
        self.geometry("1280x720")
        self.minsize(400, 400)

        # Initialize record manager if not provided
        if not hasattr(self, 'record_manager'):
            self.record_manager = RecordManager()

        # Hides notebook tabs since we are using a custom nav bar
        style = ttk.Style()
        style.layout('TNotebook.Tab', [])  # This removes the tabs

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        # Let the notebook expand vertically
        self.grid_rowconfigure(1, weight=1)

        # Create the navigation bar
        self.create_navigation_bar()

        # Create frames for each tab
        self.client_frame = ttk.Frame(self.notebook)
        self.airline_frame = ttk.Frame(self.notebook)
        self.flight_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.client_frame, text="Clients")
        self.notebook.add(self.airline_frame, text="Airlines")
        self.notebook.add(self.flight_frame, text="Flights")

        # Bind tab change event AFTER notebook is created
        self.notebook.bind("<<NotebookTabChanged>>", self.update_nav_bar)

        # Initialize GUI components
        self.client_gui = ClientGUI(self.client_frame, self.record_manager)
        self.airline_gui = AirlineGUI(self.airline_frame, self.record_manager)
        self.flight_gui = FlightGUI(self.flight_frame, self.record_manager)

        # Bind close event to save records
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # Moved the nav bar to a global nav bar instead of
    # one for each page. This is easier to manage.
    # Had to hide the default notebook nav bars as a result.
    def create_navigation_bar(self):
        """
        Create and configure the navigation bar for the application.
        Sets up buttons for switching between client, airline, and flight views,
        and manages their appearance and behavior.
        """
        nav_bar = tk.Frame(self, bg='#B3B3B3', height=50)
        nav_bar.grid(row=0, column=0, sticky='ew')
        # Don't let the nav bar expand vertically
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)  # Let it expand horizontally

        # Configure the nav_bar to expand columns evenly
        nav_bar.columnconfigure(0, weight=1)
        nav_bar.columnconfigure(1, weight=1)
        nav_bar.columnconfigure(2, weight=1)

        self.nav_labels = []  # Store references to labels
        labels = ["Client Records", "Airline Records", "Flight Records"]
        for i, text in enumerate(labels):
            # Create a frame for each button to add shadow effect
            button_frame = tk.Frame(nav_bar, bg='#888888', padx=1, pady=1)
            button_frame.grid(row=0, column=i, padx=8, pady=6, sticky='nsew')

            # Create the actual button label
            label = tk.Label(button_frame, text=text, bg='#FFFFFF', font=('Arial', 14, 'bold'),
                             padx=10, pady=5, relief='raised', bd=1)
            label.pack(fill='both', expand=True)

            # Bind events
            label.bind("<Enter>", self.on_enter)
            label.bind("<Leave>", self.on_leave)
            label.bind("<Button-1>", lambda e, i=i: self.notebook.select(i))

            self.nav_labels.append(label)

        # Bind tab change event to update navigation bar
        self.notebook.bind("<<NotebookTabChanged>>", self.update_nav_bar)

    def update_nav_bar(self, event=None):  # pylint: disable=W0613
        """Update navigation bar to highlight the selected tab"""
        selected_tab = self.notebook.index("current")
        for i, label in enumerate(self.nav_labels):
            if i == selected_tab:
                label.config(bg='#A3A3A3')  # Darker color for selected tab
            else:
                label.config(bg='#FFFFFF')  # Default color for unselected tabs

    def on_enter(self, event):
        """Change background color on hover only if not selected"""
        selected_tab = self.notebook.index("current")
        widget_index = self.nav_labels.index(event.widget)
        if widget_index != selected_tab:
            # Lighter hover color for unselected tabs
            event.widget.config(bg='#D3D3D3')

    def on_leave(self, event):
        """Reset background color when mouse leaves"""
        selected_tab = self.notebook.index("current")
        widget_index = self.nav_labels.index(event.widget)
        if widget_index != selected_tab:
            # Default color for unselected tabs
            event.widget.config(bg='#FFFFFF')
        else:
            # Keep darker color for selected tab
            event.widget.config(bg='#A3A3A3')

    def on_close(self):
        """Save records when closing the application"""
        try:
            self.record_manager.save_records()
            self.destroy()
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to save records: {str(e)}")
            self.destroy()
