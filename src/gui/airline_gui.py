"""
Module for the Airline GUI component of the Travel Agent Record Management System.
This module provides a graphical user interface for managing airline records,
including creating, reading, updating, and deleting airline information.
"""

# Imports
import tkinter as tk
from tkinter import ttk, messagebox
from data.airline import Airline


class AirlineGUI:
    """
    Graphical user interface for managing airline records.
    This class provides functionality to view, search, create, update, and delete
    airline records through a user-friendly interface with tables and forms.
    """

    def __init__(self, master, record_manager):
        self.master = master
        self.record_manager = record_manager

        # Create the main frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill='both', expand=True)

        # Initialize variables
        self.tree = None
        self.search_var = tk.StringVar()

        # Initialize update variables
        self.update_id_var = None
        self.update_company_name_var = None

        # Initialize new record variables
        self.new_company_name_var = None

        # Initialize selected_airline
        self.selected_airline = None

        # Create UI elements
        self.create_airline_records_frame()

        # Display the airline records frame directly
        self.airline_records_frame.pack(
            side='top', fill='both', expand=True, padx=10, pady=10)

        # Load existing airlines
        self.load_airlines()

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

    def create_airline_records_frame(self):
        """
        Create the main frame for displaying airline records.
        Sets up the layout for the airline records section including the title,
        buttons for CRUD operations, search functionality, and the treeview container.
        """
        # Create a frame below the navigation bar with the title "Airline Records"
        self.airline_records_frame = tk.Frame(
            self.main_frame, bg='#CCCCCC', bd=2, relief='groove')

        airline_records_title = tk.Label(
            self.airline_records_frame, text="", bg='#CCCCCC', font=('Arial', 16))
        airline_records_title.pack(side='top', pady=0)

        # Create a frame for buttons and search
        button_search_frame = tk.Frame(
            self.airline_records_frame, bg='#CCCCCC')
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
            button_frame, text="Delete", command=self.delete_airline)
        delete_button.pack(side='left', padx=20, pady=10)
        delete_button.bind("<Enter>", self.button_on_enter)
        delete_button.bind("<Leave>", self.button_on_leave)
        delete_button.bind("<Button-1>", self.button_on_click)

        # Create a frame for search field and button
        search_frame = tk.Frame(button_search_frame, bg='#CCCCCC')
        search_frame.pack(side='right', padx=5)

        search_field = tk.Entry(search_frame, width=50,
                                textvariable=self.search_var)
        self.add_placeholder(search_field, "Search Airline Record")
        search_field.pack(side='left', padx=5)

        # Allows search using enter key
        search_field.bind("<Return>", lambda event: self.search_airlines())

        # Add Clear Search button
        clear_button = tk.Button(
            search_frame, text="Clear Search", command=self.clear_search)
        clear_button.pack(side='right', padx=5, pady=5)
        clear_button.bind("<Enter>", self.button_on_enter)
        clear_button.bind("<Leave>", self.button_on_leave)
        clear_button.bind("<Button-1>", self.button_on_click)

        search_button = tk.Button(
            search_frame, text="Search", command=self.search_airlines)
        search_button.pack(side='right', padx=30, pady=5)
        search_button.bind("<Enter>", self.button_on_enter)
        search_button.bind("<Leave>", self.button_on_leave)
        search_button.bind("<Button-1>", self.button_on_click)

        # Create a Treeview widget with the specified columns
        self.create_airline_treeview()

    def create_airline_treeview(self):
        """
        Create and configure the treeview widget for displaying airline records.
        Sets up the treeview with appropriate columns, scrollbars, and event bindings
        for user interaction such as selection, double-click, and keyboard shortcuts.
        """
        columns = ("ID", "Company Name")
        self.tree = ttk.Treeview(
            self.airline_records_frame, columns=columns, show='headings')

        # Define the column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, stretch=True)

        # Add vertical and horizontal scrollbars to the Treeview
        scrollbar_y = ttk.Scrollbar(
            self.airline_records_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(
            self.airline_records_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')

        self.tree.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        # Set the background colour of the Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#D9D9D9",
                        fieldbackground="#D9D9D9")

        # Bind select event
        self.tree.bind("<<TreeviewSelect>>", self.on_airline_select)

        # Add double click to update record
        self.tree.bind(
            "<Double-1>", lambda event: self.open_update_record_modal())

        # Bind Backspace key to delete selected record
        self.tree.bind("<BackSpace>", lambda event: self.delete_airline())

        # Bind Enter key to open update modal for selected record
        self.tree.bind(
            "<Return>", lambda event: self.open_update_record_modal())

    def open_new_record_modal(self):
        """Open a modal window to create a new airline record."""
        # Create a new Toplevel window (modal)
        new_record_modal = tk.Toplevel(self.main_frame)
        new_record_modal.title("New Airline Record")
        self.center_window(new_record_modal, 700, 200)

        # Add a label to the modal
        label = tk.Label(new_record_modal,
                         text="New Airline Record", font=('Arial', 14))
        label.pack(pady=10)

        # Create a frame for the input fields
        input_frame = tk.Frame(new_record_modal)
        input_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Create entry variables
        self.new_company_name_var = tk.StringVar()

        # Add input fields to the frame
        label = tk.Label(input_frame, text="Company Name:")
        label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        entry = tk.Entry(input_frame, width=30,
                         textvariable=self.new_company_name_var)
        entry.grid(row=0, column=1, pady=5, padx=5, sticky='ew')

        # Make the input fields responsive
        input_frame.grid_columnconfigure(1, weight=1)

        # Create a frame for the buttons
        button_frame = tk.Frame(new_record_modal)
        button_frame.pack(pady=10)

        # Add Create and Cancel buttons
        create_button = tk.Button(button_frame, text="Create",
                                  command=lambda: self.create_airline_from_modal(new_record_modal))
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
        """Open a modal window to update an existing airline record."""
        # Check if an airline is selected
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "Warning", "Please select an airline to update")
            return

        # Get the selected airline
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, "values")

        try:
            airline = self.record_manager.get_airline(int(values[0]))
            if not airline:
                messagebox.showwarning("Warning", "Selected airline not found")
                return

            # Create a new Toplevel window (modal)
            update_record_modal = tk.Toplevel(self.main_frame)
            update_record_modal.title("Update Record")
            self.center_window(update_record_modal, 700, 200)

            # Add a label to the modal
            label = tk.Label(update_record_modal,
                             text="Update Record", font=('Arial', 14))
            label.pack(pady=10)

            # Create a frame for the input fields
            input_frame = tk.Frame(update_record_modal)
            input_frame.pack(pady=10, padx=10, fill='both', expand=True)

            # Create entry variables and set values
            self.update_id_var = tk.StringVar(value=airline.get_id())
            self.update_company_name_var = tk.StringVar(
                value=airline.get_company_name())

            # Add input fields to the frame
            # ID field
            label = tk.Label(input_frame, text="ID:")
            label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
            id_entry = tk.Entry(input_frame, width=30,
                                textvariable=self.update_id_var)
            id_entry.config(state='readonly')
            id_entry.grid(row=0, column=1, pady=5, padx=5, sticky='ew')

            # Company Name field
            label = tk.Label(input_frame, text="Company Name:")
            label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
            name_entry = tk.Entry(input_frame, width=30,
                                  textvariable=self.update_company_name_var)
            name_entry.grid(row=1, column=1, pady=5, padx=5, sticky='ew')

            # Make the input fields responsive
            input_frame.grid_columnconfigure(1, weight=1)

            # Create a frame for the buttons
            button_frame = tk.Frame(update_record_modal)
            button_frame.pack(pady=10)

            # Add Update and Cancel buttons
            update_button = tk.Button(button_frame, text="Update",
                                      command=lambda: self.update_airline_from_modal(
                                          airline, update_record_modal))
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

    def create_airline_from_modal(self, modal):
        """Create a new airline record from the modal form."""
        try:
            # Get values from entries
            company_name = self.new_company_name_var.get()

            # Validate required fields
            if not company_name:
                messagebox.showwarning("Warning", "Company name is required")
                return

            # Get next available ID
            next_id = self.record_manager.get_next_id("airline")

            # Create new airline object with ID
            airline = Airline(id_number=next_id, company_name=company_name)

            # Add airline to record manager
            self.record_manager.create_airline(airline)

            # Refresh airline list
            self.load_airlines()

            # Close the modal
            modal.destroy()

            messagebox.showinfo(
                "Success", f"Airline {airline.get_company_name()} created successfully!")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror(
                "Error", f"Failed to create airline: {str(e)}")

    def update_airline_from_modal(self, airline, modal):
        """Update an existing airline record from the modal form."""
        try:
            # Update airline attributes
            company_name = self.update_company_name_var.get()

            # Validate required fields
            if not company_name:
                messagebox.showwarning("Warning", "Company name is required")
                return

            airline.set_company_name(company_name)

            # Update airline in record manager
            self.record_manager.update_airline(airline)

            # Refresh airline list
            self.load_airlines()

            # Close the modal
            modal.destroy()

            messagebox.showinfo(
                "Success", f"Airline {airline.get_company_name()} updated successfully!")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror(
                "Error", f"Failed to update airline: {str(e)}")

    def delete_airline(self):
        """Delete the selected airline record."""
        # Check if an airline is selected
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "Warning", "Please select an airline to delete")
            return

        # Get the selected airline
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, "values")

        try:
            airline_id = int(values[0])
            airline = self.record_manager.get_airline(airline_id)

            if airline:
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"Are you sure you want to delete airline "
                    f"{airline.get_company_name()}?")

                if confirm:
                    # Delete airline from record manager
                    self.record_manager.delete_airline(airline_id)

                    # Refresh airline list
                    self.load_airlines()

                    messagebox.showinfo(
                        "Success", "Airline deleted successfully!")
        except ValueError as e:
            if "associated flights" in str(e):
                messagebox.showwarning(
                    "Cannot Delete",
                    f"Airline '{airline.get_company_name()}' has associated flights "
                    "and cannot be deleted. Please delete the flights first.")
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete airline: {str(e)}")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror(
                "Error", f"Failed to delete airline: {str(e)}")

    def search_airlines(self):
        """Search for airlines based on the search term."""

        # Normalize the search input
        search_term = self.search_var.get().strip()

        if not search_term:
            # If search term is empty, load all airlines
            self.load_airlines()
            return

        try:
            # Search airlines by company name
            airlines = self.record_manager.search_airlines(search_term)

            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Add search results to treeview
            for airline in airlines:
                self.tree.insert("", "end", values=(
                    airline.get_id(),
                    airline.get_company_name()
                ))
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def load_airlines(self):
        """Load all airlines from the record manager into the treeview."""
        # Check if tree exists
        if self.tree is None:
            return

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all airlines from record manager
        airlines = []
        for record in self.record_manager.records:
            if record.get("Type") == "airline":
                airline = self.record_manager.get_airline(record.get("ID"))
                if airline:
                    airlines.append(airline)

        # Add airlines to treeview
        for airline in airlines:
            self.tree.insert("", "end", values=(
                airline.get_id(),
                airline.get_company_name()
            ))

    def on_airline_select(self, event):  # pylint: disable=W0613
        """Handle airline selection in the treeview."""
        # Get selected items
        selected_items = self.tree.selection()

        # Check if any item is selected
        if not selected_items:
            return

        # Get the first selected item
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, "values")

        try:
            # Get airline from record manager
            airline = self.record_manager.get_airline(int(values[0]))

            # Store the selected airline for later use
            self.selected_airline = airline
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror(
                "Error", f"Failed to select airline: {str(e)}")

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

    def center_window(self, window, width, height):
        """Center the given window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def clear_search(self):
        """Clear the search field and reload all airlines."""
        self.search_var.set("")
        self.load_airlines()
