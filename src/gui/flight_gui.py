"""
Module for the Flight GUI component of the Travel Agent Record Management System.
This module provides a graphical user interface for managing flight records,
including creating, reading, updating, and deleting flight information.
"""


# Imports
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from data.flight import Flight
from data.client import Client
from data.airline import Airline


class FlightGUI:
    """
    Graphical user interface for managing flight records.
    This class provides functionality to view, search, create, update, and delete
    flight records through a user-friendly interface with tables and forms.
    """

    def __init__(self, master, record_manager):
        self.master = master
        self.record_manager = record_manager

        # Create the main frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill='both', expand=True)

        # Initialize variables
        self.tree = None
        self.search_start_var = tk.StringVar()
        self.search_end_var = tk.StringVar()
        self.search_date_var = tk.StringVar()
        self.search_client_var = tk.StringVar()
        self.search_airline_var = tk.StringVar()

        # Initialize client and airline variables
        self.client_var = tk.StringVar()
        self.airline_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.start_city_var = tk.StringVar()
        self.end_city_var = tk.StringVar()

        # Initialize selected flight attributes
        self.selected_flight = None
        self.selected_client_id = None
        self.selected_airline_id = None
        self.selected_date = None

        # Create UI elements
        self.create_flight_records_frame()

        # Display the flight records frame
        self.flight_records_frame.pack(
            side='top', fill='both', expand=True, padx=10, pady=10)

        # Load existing flights
        self.load_flights()

    def on_enter(self, event):
        """Change the background colour of the label when the mouse enters."""
        event.widget.config(bg='#A3A3A3')

    def on_leave(self, event):
        """Reset the background colour of the label when the mouse leaves."""
        event.widget.config(bg='#BFBFBF')

    def on_click(self, event):
        """Change the background colour of the label when it is clicked."""
        event.widget.config(bg='#A3A3A3')

    def button_on_enter(self, event):
        """Change the background colour of the button when the mouse enters."""
        event.widget.config(bg='#BFBFBF')

    def button_on_leave(self, event):
        """Reset the background colour of the button when the mouse leaves."""
        event.widget.config(bg='#F0F0F0')

    def button_on_click(self, event):
        """Change the background colour of the button when it is clicked."""
        event.widget.config(bg='#BFBFBF')

    def create_flight_records_frame(self):
        """
        Create the main frame for displaying flight records.
        Sets up the layout for the flight records section including the title,
        buttons for CRUD operations, search functionality, and the treeview container.
        """
        # Create a frame with the title "Flight Records"
        self.flight_records_frame = tk.Frame(
            self.main_frame, bg='#CCCCCC', bd=2, relief='groove')

        flight_records_title = tk.Label(
            self.flight_records_frame, text="", bg='#CCCCCC', font=('Arial', 16))
        flight_records_title.pack(side='top', pady=0)

        # Create a frame for buttons and search
        button_search_frame = tk.Frame(self.flight_records_frame, bg='#CCCCCC')
        button_search_frame.pack(side='top', pady=10, fill='x')

        # Add buttons for Create, Update, and Delete
        button_frame = tk.Frame(button_search_frame, bg='#CCCCCC')
        button_frame.pack(side='left', padx=5)

        create_button = tk.Button(
            button_frame, text="Create", command=self.open_new_record_modal)
        create_button.pack(side='left', padx=20, pady=10)
        create_button.bind("<Enter>", self.button_on_enter)
        create_button.bind("<Leave>", self.button_on_leave)
        create_button.bind("<Button-1>", self.button_on_click)

        update_button = tk.Button(
            button_frame, text="Update", command=self.open_update_record_modal)
        update_button.pack(side='left', padx=10, pady=10)
        update_button.bind("<Enter>", self.button_on_enter)
        update_button.bind("<Leave>", self.button_on_leave)
        update_button.bind("<Button-1>", self.button_on_click)

        delete_button = tk.Button(
            button_frame, text="Delete", command=self.delete_flight)
        delete_button.pack(side='left', padx=20, pady=10)
        delete_button.bind("<Enter>", self.button_on_enter)
        delete_button.bind("<Leave>", self.button_on_leave)
        delete_button.bind("<Button-1>", self.button_on_click)

        # Create a frame for search fields and button
        search_frame = tk.Frame(button_search_frame, bg='#CCCCCC')
        search_frame.pack(side='right', padx=5)

        # Add search fields (first row)
        ttk.Label(search_frame, text="Start City:").grid(
            row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(
            search_frame, textvariable=self.search_start_var, width=20)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        start_entry.bind("<Return>", lambda event: self.search_flights())

        ttk.Label(search_frame, text="End City:").grid(
            row=0, column=2, padx=5, pady=5)
        end_entry = tk.Entry(
            search_frame, textvariable=self.search_end_var, width=20)
        end_entry.grid(row=0, column=3, padx=5, pady=5)
        end_entry.bind("<Return>", lambda event: self.search_flights())

        ttk.Label(search_frame, text="Date:").grid(
            row=0, column=4, padx=5, pady=5)
        date_entry = DateEntry(search_frame, width=20, background='darkblue',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                               textvariable=self.search_date_var)
        date_entry.delete(0, 'end')  # Clear the default date
        date_entry.grid(row=0, column=5, padx=5, pady=5)
        date_entry.bind("<Return>", lambda event: self.search_flights())

        # Add client and airline dropdowns (second row)
        ttk.Label(search_frame, text="Client:").grid(
            row=1, column=0, padx=5, pady=5)
        client_combo = ttk.Combobox(
            search_frame, textvariable=self.search_client_var,
            state="readonly", width=40,
            postcommand=lambda: self.populate_client_combo(client_combo))
        client_combo.grid(row=1, column=1, columnspan=2,
                          padx=5, pady=5, sticky='ew')
        self.populate_client_combo(client_combo)
        client_combo.set("")  # Default empty selection

        ttk.Label(search_frame, text="Airline:").grid(
            row=1, column=3, padx=5, pady=5)
        airline_combo = ttk.Combobox(
            search_frame, textvariable=self.search_airline_var,
            state="readonly", width=40,
            postcommand=lambda: self.populate_airline_combo(airline_combo))
        airline_combo.grid(row=1, column=4, columnspan=2,
                           padx=5, pady=5, sticky='ew')
        self.populate_airline_combo(airline_combo)
        airline_combo.set("")  # Default empty selection

        # Add search and clear buttons (second row)
        search_button = tk.Button(
            search_frame, text="Search", command=self.search_flights)
        search_button.grid(row=1, column=6, padx=5, pady=5)
        search_button.bind("<Enter>", self.button_on_enter)
        search_button.bind("<Leave>", self.button_on_leave)
        search_button.bind("<Button-1>", self.button_on_click)

        clear_button = tk.Button(
            search_frame, text="Clear Search", command=self.clear_search_fields)
        clear_button.grid(row=1, column=7, padx=5, pady=5)
        clear_button.bind("<Enter>", self.button_on_enter)
        clear_button.bind("<Leave>", self.button_on_leave)
        clear_button.bind("<Button-1>", self.button_on_click)

        # Create a Treeview widget with the specified columns
        self.create_flight_treeview()

    def clear_search_fields(self):
        """Clear all search fields and reload all flights."""
        self.search_start_var.set('')
        self.search_end_var.set('')
        self.search_date_var.set('')
        self.search_client_var.set('')
        self.search_airline_var.set('')

        # Reset the DateEntry widget to its default state
        for widget in self.flight_records_frame.winfo_children():
            if isinstance(widget, DateEntry):
                widget.set_date(datetime.now())

        self.load_flights()

    def create_flight_treeview(self):
        """
        Create and configure the treeview widget for displaying flight records.
        Sets up the treeview with appropriate columns, scrollbars, and event bindings
        for user interaction such as selection, double-click, and keyboard shortcuts.
        """
        columns = ("Client", "Airline", "Date", "Start City", "End City")
        self.tree = ttk.Treeview(
            self.flight_records_frame, columns=columns, show='headings')

        # Define the column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, stretch=True)

        # Add vertical and horizontal scrollbars to the Treeview
        scrollbar_y = ttk.Scrollbar(
            self.flight_records_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(
            self.flight_records_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')

        self.tree.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        # Set the background colour of the Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#D9D9D9",
                        fieldbackground="#D9D9D9")

        # Bind select event
        self.tree.bind("<<TreeviewSelect>>", self.on_flight_select)

        # Bind double click to update event
        self.tree.bind(
            "<Double-1>", lambda event: self.open_update_record_modal())

        # Bind Backspace key to delete selected record
        self.tree.bind("<BackSpace>", lambda event: self.delete_flight())

        # Bind Enter key to open update modal for selected record
        self.tree.bind(
            "<Return>", lambda event: self.open_update_record_modal())

    def open_new_record_modal(self):
        """Open a modal window to create a new flight record."""
        # Reset input variables
        self.client_var.set('')
        self.airline_var.set('')
        self.date_var.set('')
        self.start_city_var.set('')
        self.end_city_var.set('')

        # Create a new Toplevel window (modal)
        new_record_modal = tk.Toplevel(self.main_frame)
        new_record_modal.title("New Flight Record")
        self.center_window(new_record_modal, 700, 200)

        # Add a label to the modal
        label = tk.Label(new_record_modal,
                         text="New Flight Record", font=('Arial', 14))
        label.pack(pady=10)

        # Create a frame for the input fields
        input_frame = tk.Frame(new_record_modal)
        input_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Add combo boxes for Client ID and Airline ID
        client_id_label = tk.Label(input_frame, text="Client:")
        client_id_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        client_combo = ttk.Combobox(
            input_frame, textvariable=self.client_var,
            state="readonly",
            postcommand=lambda: self.populate_client_combo(client_combo))
        client_combo.grid(row=0, column=1, pady=5, padx=5, sticky='ew')
        self.populate_client_combo(client_combo)

        airline_id_label = tk.Label(input_frame, text="Airline:")
        airline_id_label.grid(row=0, column=2, sticky='e', pady=5, padx=5)
        airline_combo = ttk.Combobox(
            input_frame, textvariable=self.airline_var,
            state="readonly",
            postcommand=lambda: self.populate_airline_combo(airline_combo))
        airline_combo.grid(row=0, column=3, pady=5, padx=5, sticky='ew')
        self.populate_airline_combo(airline_combo)

        # Date field
        date_label = tk.Label(input_frame, text="Date:")
        date_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
        date_entry = DateEntry(input_frame, width=12, background='darkblue',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                               textvariable=self.date_var)
        date_entry.grid(row=1, column=1, pady=5, padx=5, sticky='ew')

        # Start City field
        start_city_label = tk.Label(input_frame, text="Start City:")
        start_city_label.grid(row=1, column=2, sticky='e', pady=5, padx=5)
        start_city_entry = tk.Entry(
            input_frame, textvariable=self.start_city_var, width=30)
        start_city_entry.grid(row=1, column=3, pady=5, padx=5, sticky='ew')

        # End City field
        end_city_label = tk.Label(input_frame, text="End City:")
        end_city_label.grid(row=2, column=0, sticky='e', pady=5, padx=5)
        end_city_entry = tk.Entry(
            input_frame, textvariable=self.end_city_var, width=30)
        end_city_entry.grid(row=2, column=1, pady=5, padx=5, sticky='ew')

        # Make the input fields responsive
        for i in range(4):
            input_frame.grid_columnconfigure(i, weight=1)

        # Create a frame for the buttons
        button_frame = tk.Frame(new_record_modal)
        button_frame.pack(pady=10)

        # Add Create and Cancel buttons
        create_button = tk.Button(button_frame, text="Create",
                                  command=lambda: self.create_flight_from_modal(new_record_modal))
        create_button.pack(side='left', padx=5)
        create_button.bind("<Enter>", self.button_on_enter)
        create_button.bind("<Leave>", self.button_on_leave)
        create_button.bind("<Button-1>", self.button_on_click)

        cancel_button = tk.Button(
            button_frame, text="Cancel", command=new_record_modal.destroy)
        cancel_button.pack(side='left', padx=5)
        cancel_button.bind("<Enter>", self.button_on_enter)
        cancel_button.bind("<Leave>", self.button_on_leave)
        cancel_button.bind("<Button-1>", self.button_on_click)

        # Make the modal window modal (block interaction with the main window)
        new_record_modal.transient(self.main_frame)
        new_record_modal.grab_set()
        self.main_frame.wait_window(new_record_modal)

    def open_update_record_modal(self):
        """Open a modal window to update an existing flight record."""
        # Check if a flight is selected
        if not self.selected_flight:
            messagebox.showwarning(
                "Warning", "Please select a flight to update")
            return

        try:
            # Get values from the selected flight record
            client_id = self.selected_flight.get("Client_ID")
            airline_id = self.selected_flight.get("Airline_ID")
            date_str = self.selected_flight.get("Date")
            start_city = self.selected_flight.get("Start City")
            end_city = self.selected_flight.get("End City")

            # Create Flight object from the record
            flight = Flight.from_dict(self.selected_flight)

            # Create a new Toplevel window (modal)
            update_record_modal = tk.Toplevel(self.main_frame)
            update_record_modal.title("Update Flight Record")
            self.center_window(update_record_modal, 700, 200)

            # Add a label to the modal
            label = tk.Label(update_record_modal,
                             text="Update Flight Record", font=('Arial', 14))
            label.pack(pady=10)

            # Create a frame for the input fields
            input_frame = tk.Frame(update_record_modal)
            input_frame.pack(pady=10, padx=10, fill='both', expand=True)

            # Get client and airline names for display
            client = self.record_manager.get_client(client_id)
            airline = self.record_manager.get_airline(airline_id)
            client_name = client.get_name() if client else "Unknown"
            airline_name = airline.get_company_name() if airline else "Unknown"

            # Format date for display - extract just the date part if ISO format
            display_date = date_str.split(
                "T")[0] if "T" in date_str else date_str

            # Set current values
            self.client_var.set(f"{client_id} - {client_name}")
            self.airline_var.set(f"{airline_id} - {airline_name}")
            self.date_var.set(display_date)
            self.start_city_var.set(start_city)
            self.end_city_var.set(end_city)

            # Add combo boxes for Client ID and Airline ID
            client_id_label = tk.Label(input_frame, text="Client:")
            client_id_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
            client_combo = ttk.Combobox(
                input_frame, textvariable=self.client_var,
                state="readonly",
                postcommand=lambda: self.populate_client_combo(client_combo))
            client_combo.grid(row=0, column=1, pady=5, padx=5, sticky='ew')
            self.populate_client_combo(client_combo)

            airline_id_label = tk.Label(input_frame, text="Airline:")
            airline_id_label.grid(row=0, column=2, sticky='e', pady=5, padx=5)
            airline_combo = ttk.Combobox(
                input_frame, textvariable=self.airline_var,
                state="readonly",
                postcommand=lambda: self.populate_airline_combo(airline_combo))
            airline_combo.grid(row=0, column=3, pady=5, padx=5, sticky='ew')
            self.populate_airline_combo(airline_combo)

            # Date field
            date_label = tk.Label(input_frame, text="Date:")
            date_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
            date_entry = DateEntry(input_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2,
                                   date_pattern='yyyy-mm-dd',
                                   textvariable=self.date_var)
            date_entry.set_date(datetime.strptime(display_date, "%Y-%m-%d"))
            date_entry.grid(row=1, column=1, pady=5, padx=5, sticky='ew')

            # Start City field
            start_city_label = tk.Label(input_frame, text="Start City:")
            start_city_label.grid(row=1, column=2, sticky='e', pady=5, padx=5)
            start_city_entry = tk.Entry(
                input_frame, textvariable=self.start_city_var, width=30)
            start_city_entry.grid(row=1, column=3, pady=5, padx=5, sticky='ew')

            # End City field
            end_city_label = tk.Label(input_frame, text="End City:")
            end_city_label.grid(row=2, column=0, sticky='e', pady=5, padx=5)
            end_city_entry = tk.Entry(
                input_frame, textvariable=self.end_city_var, width=30)
            end_city_entry.grid(row=2, column=1, pady=5, padx=5, sticky='ew')

            # Make the input fields responsive
            for i in range(4):
                input_frame.grid_columnconfigure(i, weight=1)

            # Create a frame for the buttons
            button_frame = tk.Frame(update_record_modal)
            button_frame.pack(pady=10)

            # Add Update and Cancel buttons
            update_button = tk.Button(
                button_frame, text="Update",
                command=lambda: self.update_flight_from_modal(
                    flight, update_record_modal))
            update_button.pack(side='left', padx=5)
            update_button.bind("<Enter>", self.button_on_enter)
            update_button.bind("<Leave>", self.button_on_leave)
            update_button.bind("<Button-1>", self.button_on_click)

            cancel_button = tk.Button(
                button_frame, text="Cancel", command=update_record_modal.destroy)
            cancel_button.pack(side='left', padx=5)
            cancel_button.bind("<Enter>", self.button_on_enter)
            cancel_button.bind("<Leave>", self.button_on_leave)
            cancel_button.bind("<Button-1>", self.button_on_click)

            # Make the modal window modal (block interaction with the main window)
            update_record_modal.transient(self.main_frame)
            update_record_modal.grab_set()
            self.main_frame.wait_window(update_record_modal)

        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror(
                "Error", f"Failed to open update modal: {str(e)}")

    def create_flight_from_modal(self, modal):
        """Create a new flight record from the modal form."""
        try:
            # Get values from entries
            if not self.client_var.get() or not self.airline_var.get() \
                    or not self.date_var.get() or not self.start_city_var.get() \
                    or not self.end_city_var.get():
                messagebox.showwarning("Warning", "All fields are required")
                return

            # Parse client ID and airline ID
            client_id = int(self.client_var.get().split(" - ")[0])
            airline_id = int(self.airline_var.get().split(" - ")[0])

            # Check if date is in correct format
            date_str = self.date_var.get()
            if self.is_placeholder(date_str, "YYYY-MM-DD"):
                date_str = ""

            # Create new flight object
            flight = Flight(
                client_id=client_id,
                airline_id=airline_id,
                date=date_str,
                start_city=self.start_city_var.get(),
                end_city=self.end_city_var.get()
            )

            # Add flight to record manager
            self.record_manager.create_flight(flight)

            # Refresh flight list
            self.load_flights()

            # Close the modal
            modal.destroy()

            messagebox.showinfo("Success", "Flight created successfully!")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to create flight: {str(e)}")

    def update_flight_from_modal(self, flight, modal):
        """Update an existing flight record from the modal form."""
        try:
            # Get values from entries
            if not self.client_var.get() or not self.airline_var.get() \
                    or not self.date_var.get() or not self.start_city_var.get() \
                    or not self.end_city_var.get():
                messagebox.showwarning("Warning", "All fields are required")
                return

            # Parse client ID and airline ID
            new_client_id = int(self.client_var.get().split(" - ")[0])
            new_airline_id = int(self.airline_var.get().split(" - ")[0])

            # Store original values for finding the record to update
            original_client_id = flight.get_client_id()
            original_airline_id = flight.get_airline_id()
            original_date = flight.get_date()

            # Update flight attributes
            flight.set_client_id(new_client_id)
            flight.set_airline_id(new_airline_id)
            flight.set_date(self.date_var.get())
            flight.set_start_city(self.start_city_var.get())
            flight.set_end_city(self.end_city_var.get())

            # Update flight in record manager with original values to find the correct record
            self.record_manager.update_flight(
                flight, original_client_id, original_airline_id, original_date)

            # Refresh flight list
            self.load_flights()

            # Close the modal
            modal.destroy()

            messagebox.showinfo("Success", "Flight updated successfully!")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to update flight: {str(e)}")

    def delete_flight(self):
        """Delete the selected flight record."""
        # Check if a flight is selected
        if not self.selected_flight:
            messagebox.showwarning(
                "Warning", "Please select a flight to delete")
            return

        try:
            # Get values from the selected flight record
            client_id = self.selected_flight.get("Client_ID")
            airline_id = self.selected_flight.get("Airline_ID")
            date_str = self.selected_flight.get("Date")
            start_city = self.selected_flight.get("Start City")
            end_city = self.selected_flight.get("End City")

            # Get client and airline names for better confirmation message
            client = self.record_manager.get_client(client_id)
            airline = self.record_manager.get_airline(airline_id)
            client_name = client.get_name() if client else "Unknown"
            airline_name = airline.get_company_name() if airline else "Unknown"

            # Format date for display (remove time part if present)
            display_date = date_str.split(
                "T")[0] if "T" in date_str else date_str

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the flight from {start_city} to {end_city} "
                f"on {display_date} for client {client_name} with {airline_name}?")

            if not confirm:
                return

            # Use record manager to delete the flight with the exact values
            success = self.record_manager.delete_flight(
                client_id, airline_id, date_str)

            if success:
                # Refresh flight list
                self.load_flights()
                messagebox.showinfo("Success", "Flight deleted successfully!")
            else:
                messagebox.showerror(
                    "Error", "Could not find the flight record to delete")

        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to delete flight: {str(e)}")

    def search_flights(self):
        """Search for flights based on the search criteria."""
        start_city = self.search_start_var.get().strip()
        end_city = self.search_end_var.get().strip()
        date = self.search_date_var.get().strip()

        # Get client_id and airline_id from dropdown selections if available
        client_selection = self.search_client_var.get() if \
            hasattr(self, 'search_client_var') else ""
        airline_selection = self.search_airline_var.get() if \
            hasattr(self, 'search_airline_var') else ""

        # Extract IDs from selections
        client_id = None
        airline_id = None

        if client_selection:
            try:
                client_id = int(client_selection.split(" - ")[0])
            except (ValueError, IndexError):
                pass

        if airline_selection:
            try:
                airline_id = int(airline_selection.split(" - ")[0])
            except (ValueError, IndexError):
                pass

        # If all search terms are empty, load all flights
        if not start_city and not end_city and not date and not client_id and not airline_id:
            self.load_flights()
            return

        try:
            # Validate date format if provided
            search_date = None
            if date:
                try:
                    search_date = datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(
                        "Error", "Invalid date format. Use YYYY-MM-DD.")
                    return

            # Get all flights from record manager
            flights = []
            for record in self.record_manager.records:
                if record.get("Type") == "flight":
                    flight = Flight.from_dict(record)

                    # Filter by criteria
                    match = True

                    # Check client ID
                    if client_id and flight.get_client_id() != client_id:
                        match = False

                    # Check airline ID
                    if airline_id and flight.get_airline_id() != airline_id:
                        match = False

                    # Check start city
                    if start_city and start_city.lower() not in flight.get_start_city().lower():
                        match = False

                    # Check end city
                    if end_city and end_city.lower() not in flight.get_end_city().lower():
                        match = False

                    # Check date
                    if search_date:
                        flight_date = flight.get_date()
                        if isinstance(flight_date, str):
                            # Convert string date to datetime for comparison
                            try:
                                if 'T' in flight_date:
                                    flight_date = datetime.fromisoformat(
                                        flight_date)
                                else:
                                    flight_date = datetime.strptime(
                                        flight_date, "%Y-%m-%d")
                            except (ValueError, TypeError):
                                match = False
                                continue

                        # Compare dates (ignoring time)
                        if isinstance(flight_date, datetime) and flight_date.date() \
                                != search_date.date():
                            match = False

                    if match:
                        flights.append(flight)

            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Add search results to treeview
            for flight in flights:
                # Get client and airline names
                client = self.record_manager.get_client(flight.get_client_id())
                airline = self.record_manager.get_airline(
                    flight.get_airline_id())

                client_name = client.get_name() if client else "Unknown"
                airline_name = airline.get_company_name() if airline else "Unknown"

                # Format date
                date_str = flight.get_date()
                if isinstance(date_str, datetime):
                    date_str = date_str.strftime("%Y-%m-%d")

                self.tree.insert("", "end", values=(
                    f"{flight.get_client_id()} - {client_name}",
                    f"{flight.get_airline_id()} - {airline_name}",
                    date_str,
                    flight.get_start_city(),
                    flight.get_end_city()
                ))

            # Show message if no results found
            if not flights:
                messagebox.showinfo(
                    "Search Results", "No flights found matching the criteria.")

        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def load_flights(self):
        """Load all flights from the record manager into the treeview."""
        # Check if tree exists
        if self.tree is None:
            return

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all flights from record manager
        flights = []
        for record in self.record_manager.records:
            if record.get("Type") == "flight":
                client_id = record.get("Client_ID")
                airline_id = record.get("Airline_ID")

                # Get client and airline objects using record manager
                client = self.record_manager.get_client(client_id)
                airline = self.record_manager.get_airline(airline_id)

                if client and airline:
                    flight = Flight.from_dict(record)
                    flights.append((flight, client, airline))

        # Add flights to treeview
        for flight, client, airline in flights:
            # Format date
            date_str = flight.get_date()
            if isinstance(date_str, datetime):
                date_str = date_str.strftime("%Y-%m-%d")

            self.tree.insert("", "end", values=(
                f"{flight.get_client_id()} - {client.get_name()}",
                f"{flight.get_airline_id()} - {airline.get_company_name()}",
                date_str,
                flight.get_start_city(),
                flight.get_end_city()
            ))

    def on_flight_select(self, event):  # pylint: disable=W0613
        """Handle flight selection in the treeview."""
        # Get selected items
        selected_items = self.tree.selection()

        # Clear previous selection
        self.selected_flight = None

        # Check if any item is selected
        if not selected_items:
            return

        # Get the first selected item
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, "values")

        try:
            # Parse client ID and airline ID from values
            client_id = int(values[0].split(" - ")[0])
            airline_id = int(values[1].split(" - ")[0])

            # Find the original flight record
            for record in self.record_manager.records:
                if (record.get("Type") == "flight" and
                    record.get("Client_ID") == client_id and
                        record.get("Airline_ID") == airline_id):
                    # Store the entire record
                    self.selected_flight = record
                    break
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to select flight: {str(e)}")

    def populate_client_combo(self, combo):
        """Populate the client combo box with client names."""
        # Get all clients from record manager
        clients = []
        for record in self.record_manager.records:
            if record.get("Type") == "client":
                client = Client.from_dict(record)
                clients.append((client.get_id(), client.get_name()))

        # Sort clients by name
        clients.sort(key=lambda x: x[1])

        # Update combobox values
        combo['values'] = [f"{id} - {name}" for id, name in clients]

    def populate_airline_combo(self, combo):
        """Populate the airline combo box with airline names."""
        # Get all airlines from record manager
        airlines = []
        for record in self.record_manager.records:
            if record.get("Type") == "airline":
                airline = Airline.from_dict(record)
                airlines.append((airline.get_id(), airline.get_company_name()))

        # Sort airlines by name
        airlines.sort(key=lambda x: x[1])

        # Update combobox values
        combo['values'] = [f"{id} - {name}" for id, name in airlines]

    def add_placeholder(self, entry, placeholder):
        """Add a placeholder to the given entry widget."""
        entry.insert(0, placeholder)
        entry.config(fg='grey')
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(
            event, placeholder))
        entry.bind("<FocusOut>", lambda event: self.set_placeholder(
            event, placeholder))

    def clear_placeholder(self, event, placeholder):
        """Clear the placeholder from the given entry widget."""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg='black')

    def set_placeholder(self, event, placeholder):
        """Set the placeholder in the given entry widget."""
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg='grey')

    def is_placeholder(self, text, placeholder):
        """Check if the text is a placeholder."""
        return text == placeholder

    def center_window(self, window, width, height):
        """Center the given window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
