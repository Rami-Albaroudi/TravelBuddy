"""
Module for the Client GUI component of the Travel Agent Record Management System.
This module provides a graphical user interface for managing client records,
including creating, reading, updating, and deleting client information.
"""

# Imports
import tkinter as tk
from tkinter import ttk, messagebox
from data.client import Client


class ClientGUI:
    """
    Graphical user interface for managing client records.
    This class provides functionality to view, search, create, update, and delete
    client records through a user-friendly interface with tables and forms.
    It handles all client-related operations including validation and error handling.
    """

    def __init__(self, master, record_manager):
        self.master = master
        self.record_manager = record_manager

        # Initialize selected_client
        self.selected_client = None

        # Initialize StringVar attributes for modals
        self.new_name_var = None
        self.new_addr1_var = None
        self.new_addr2_var = None
        self.new_addr3_var = None
        self.new_city_var = None
        self.new_state_var = None
        self.new_zip_var = None
        self.new_country_var = None
        self.new_phone_var = None
        self.update_id_var = None
        self.update_name_var = None
        self.update_addr1_var = None
        self.update_addr2_var = None
        self.update_addr3_var = None
        self.update_city_var = None
        self.update_state_var = None
        self.update_zip_var = None
        self.update_country_var = None
        self.update_phone_var = None

        # Initialize tree attribute
        self.tree = None

        # Create the main frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill='both', expand=True)

        # Create UI elements
        self.create_client_records_frame()

        # Display the airline records frame directly
        self.client_records_frame.pack(
            side='top', fill='both', expand=True, padx=10, pady=10)

        # Load existing clients
        self.load_clients()

    def create_client_treeview(self):
        """
        Create and configure the treeview widget for displaying client records.
        Sets up the treeview with appropriate columns, scrollbars, and event bindings
        for user interaction such as selection, double-click, and keyboard shortcuts.
        """
        columns = ("ID", "Name", "Address Line 1", "Address Line 2",
                   "Address Line 3", "City", "State", "Zip Code", "Country", "Phone Number")
        self.tree = ttk.Treeview(
            self.client_records_frame, columns=columns, show='headings')

        # Define the column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, stretch=True)

        # Add vertical and horizontal scrollbars to the Treeview
        scrollbar_y = ttk.Scrollbar(
            self.client_records_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(
            self.client_records_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')

        self.tree.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        # Set the background colour of the Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#D9D9D9",
                        fieldbackground="#D9D9D9")

        # Bind select event
        self.tree.bind("<<TreeviewSelect>>", self.on_client_select)

        # Bind double click to update event
        self.tree.bind(
            "<Double-1>", lambda event: self.open_update_record_modal())

        # Bind Backspace key to delete selected record
        self.tree.bind("<BackSpace>", lambda event: self.delete_client())

        # Bind Enter key to open update modal for selected record
        self.tree.bind(
            "<Return>", lambda event: self.open_update_record_modal())

    # Event handlers for label hover and click events
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

    def create_client_records_frame(self):
        """
        Create the main frame for displaying client records.
        Sets up the layout for the client records section including the title,
        buttons for CRUD operations, search functionality, and the treeview container.
        """
        # Create a frame below the navigation bar with the title "Client Records"
        self.client_records_frame = tk.Frame(
            self.main_frame, bg='#CCCCCC', bd=2, relief='groove')

        client_records_title = tk.Label(
            self.client_records_frame, text="", bg='#CCCCCC', font=('Arial', 16))
        client_records_title.pack(side='top', pady=0)

        # Create a frame for buttons and search
        button_search_frame = tk.Frame(self.client_records_frame, bg='#CCCCCC')
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
            button_frame, text="Delete", command=self.delete_client)
        delete_button.pack(side='left', padx=20, pady=10)
        delete_button.bind("<Enter>", self.button_on_enter)
        delete_button.bind("<Leave>", self.button_on_leave)
        delete_button.bind("<Button-1>", self.button_on_click)

        # Create a frame for search field and button
        search_frame = tk.Frame(button_search_frame, bg='#CCCCCC')
        search_frame.pack(side='right', padx=5)

        self.search_var = tk.StringVar()
        search_field = tk.Entry(search_frame, width=50,
                                textvariable=self.search_var)
        self.add_placeholder(search_field, "Search Client Record")
        search_field.pack(side='left', padx=5)

        # Add the Clear Search button
        clear_button = tk.Button(
            search_frame, text="Clear Search", command=self.clear_search)
        clear_button.pack(side='right', padx=5, pady=5)
        clear_button.bind("<Enter>", self.button_on_enter)
        clear_button.bind("<Leave>", self.button_on_leave)
        clear_button.bind("<Button-1>", self.button_on_click)

        search_button = tk.Button(
            search_frame, text="Search", command=self.search_clients)
        search_button.pack(side='right', padx=30, pady=5)
        search_button.bind("<Enter>", self.button_on_enter)
        search_button.bind("<Leave>", self.button_on_leave)
        search_button.bind("<Button-1>", self.button_on_click)

        search_field.bind("<Return>", lambda event: self.search_clients())

        # Create a Treeview widget with the specified columns
        self.create_client_treeview()

    def open_new_record_modal(self):
        """Open a modal window to create a new client record."""
        # Create a new Toplevel window (modal)
        new_record_modal = tk.Toplevel(self.main_frame)
        new_record_modal.title("New Client Record")
        self.center_window(new_record_modal, 700, 300)

        # Add a label to the modal
        label = tk.Label(new_record_modal,
                         text="New Client Record", font=('Arial', 14))
        label.pack(pady=10)

        # Create a frame for the input fields
        input_frame = tk.Frame(new_record_modal)
        input_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Define the input fields
        fields = [
            "Given Name(s)", "Family Name", "Address Line 1", "Address Line 2",
            "Address Line 3", "City", "State", "Zip Code", "Country", "Phone Number"
        ]

        placeholders = {
            "Given Name(s)": "First and middle name",
            "Address Line 1": "Street name",
            "Address Line 2": "Street or civic number",
            "Address Line 3": "Apartment, suite, unit number, PO Box",
            "Phone Number": "Include country code"
        }

        # Create entry variables
        self.new_name_var = tk.StringVar()
        self.new_addr1_var = tk.StringVar()
        self.new_addr2_var = tk.StringVar()
        self.new_addr3_var = tk.StringVar()
        self.new_city_var = tk.StringVar()
        self.new_state_var = tk.StringVar()
        self.new_zip_var = tk.StringVar()
        self.new_country_var = tk.StringVar()
        self.new_phone_var = tk.StringVar()

        entry_vars = {
            "Given Name(s)": self.new_name_var,
            "Family Name": tk.StringVar(),  # This will be combined with Given Name(s)
            "Address Line 1": self.new_addr1_var,
            "Address Line 2": self.new_addr2_var,
            "Address Line 3": self.new_addr3_var,
            "City": self.new_city_var,
            "State": self.new_state_var,
            "Zip Code": self.new_zip_var,
            "Country": self.new_country_var,
            "Phone Number": self.new_phone_var
        }

        # Add input fields to the frame, two fields per line
        entries = {}
        for i, field in enumerate(fields):
            label = tk.Label(input_frame, text=f"{field}:")
            label.grid(row=i//2, column=(i % 2)*2, sticky='e', pady=5, padx=5)
            entry = tk.Entry(input_frame, width=30,
                             textvariable=entry_vars[field])
            entry.grid(row=i//2, column=(i % 2)*2+1,
                       pady=5, padx=5, sticky='ew')
            entries[field] = entry
            if field in placeholders:
                self.add_placeholder(entry, placeholders[field])

        # Make the input fields responsive
        for i in range(2):
            input_frame.grid_columnconfigure(i*2+1, weight=1)

        # Create a frame for the buttons
        button_frame = tk.Frame(new_record_modal)
        button_frame.pack(pady=10)

        # Add Create and Cancel buttons
        create_button = tk.Button(button_frame, text="Create",
                                  command=lambda: self.create_client_from_modal(
                                      entries, new_record_modal))
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
        """Open a modal window to update an existing client record."""
        # Check if a client is selected
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "Warning", "Please select a client to update")
            return

        # Get the selected client
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, "values")

        try:
            client = self.record_manager.get_client(int(values[0]))
            if not client:
                messagebox.showwarning("Warning", "Selected client not found")
                return

            # Create a new Toplevel window (modal)
            update_record_modal = tk.Toplevel(self.main_frame)
            update_record_modal.title("Update Record")
            self.center_window(update_record_modal, 700, 300)

            # Add a label to the modal
            label = tk.Label(update_record_modal,
                             text="Update Record", font=('Arial', 14))
            label.pack(pady=10)

            # Create a frame for the input fields
            input_frame = tk.Frame(update_record_modal)
            input_frame.pack(pady=10, padx=10, fill='both', expand=True)

            # Define the input fields
            fields = [
                "ID", "Name", "Address Line 1", "Address Line 2",
                "Address Line 3", "City", "State", "Zip Code", "Country", "Phone Number"
            ]

            # Create entry variables and set values teassign StringVar instances with values
            self.update_id_var = tk.StringVar(value=client.get_id())
            self.update_name_var = tk.StringVar(value=client.get_name())
            self.update_addr1_var = tk.StringVar(
                value=client.get_address_line_1())
            self.update_addr2_var = tk.StringVar(
                value=client.get_address_line_2())
            self.update_addr3_var = tk.StringVar(
                value=client.get_address_line_3())
            self.update_city_var = tk.StringVar(value=client.get_city())
            self.update_state_var = tk.StringVar(value=client.get_state())
            self.update_zip_var = tk.StringVar(value=client.get_zip_code())
            self.update_country_var = tk.StringVar(value=client.get_country())
            self.update_phone_var = tk.StringVar(
                value=client.get_phone_number())

            entry_vars = {
                "ID": self.update_id_var,
                "Name": self.update_name_var,
                "Address Line 1": self.update_addr1_var,
                "Address Line 2": self.update_addr2_var,
                "Address Line 3": self.update_addr3_var,
                "City": self.update_city_var,
                "State": self.update_state_var,
                "Zip Code": self.update_zip_var,
                "Country": self.update_country_var,
                "Phone Number": self.update_phone_var
            }

            # Add input fields to the frame, two fields per line
            for i, field in enumerate(fields):
                label = tk.Label(input_frame, text=f"{field}:")
                label.grid(row=i//2, column=(i % 2)*2,
                           sticky='e', pady=5, padx=5)
                entry = tk.Entry(input_frame, width=30,
                                 textvariable=entry_vars[field])
                if field == "ID":
                    entry.config(state='readonly')
                entry.grid(row=i//2, column=(i % 2)*2+1,
                           pady=5, padx=5, sticky='ew')

            # Make the input fields responsive
            for i in range(2):
                input_frame.grid_columnconfigure(i*2+1, weight=1)

            # Create a frame for the buttons
            button_frame = tk.Frame(update_record_modal)
            button_frame.pack(pady=10)

            # Add Update and Cancel buttons
            update_button = tk.Button(button_frame, text="Update",
                                      command=lambda: self.update_client_from_modal(
                                          client, update_record_modal))
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

    def create_client_from_modal(self, entries, modal):
        """Create a new client record from the modal form."""
        try:
            # Get values from entries, replacing placeholders with empty strings
            given_name = self.get_entry_value(
                entries["Given Name(s)"], "First and Middle Name")
            family_name = self.get_entry_value(
                entries["Family Name"], "Last Name")

            # Combine and check if empty
            name = f"{given_name} {family_name}".strip()

            if not name:
                messagebox.showwarning("Warning", "Name is required")
                return

            # Get next available ID
            next_id = self.record_manager.get_next_id("client")

            # Create new client object
            client = Client(
                id_number=next_id,
                name=name,
                address_line_1=self.get_entry_value(
                    entries["Address Line 1"], "Street name"),
                address_line_2=self.get_entry_value(
                    entries["Address Line 2"], "Street or civic number"),
                address_line_3=self.get_entry_value(
                    entries["Address Line 3"], "Apartment, suite, unit number, PO Box"),
                city=self.get_entry_value(entries["City"], "City"),
                state=self.get_entry_value(
                    entries["State"], "State or Province"),
                zip_code=self.get_entry_value(
                    entries["Zip Code"], "Zip or Postal Code"),
                country=self.get_entry_value(entries["Country"], "Country"),
                phone_number=self.get_entry_value(
                    entries["Phone Number"], "Include country code")
            )

            # Add client to record manager
            self.record_manager.create_client(client)

            # Refresh client list
            self.load_clients()

            # Close the modal
            modal.destroy()

            messagebox.showinfo(
                "Success", f"Client {client.get_name()} created successfully!")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to create client: {str(e)}")

    def update_client_from_modal(self, client, modal):
        """Update an existing client record from the modal form."""
        try:
            # Update client attributes
            client.set_name(self.update_name_var.get())
            client.set_address_line_1(self.update_addr1_var.get())
            client.set_address_line_2(self.update_addr2_var.get())
            client.set_address_line_3(self.update_addr3_var.get())
            client.set_city(self.update_city_var.get())
            client.set_state(self.update_state_var.get())
            client.set_zip_code(self.update_zip_var.get())
            client.set_country(self.update_country_var.get())
            client.set_phone_number(self.update_phone_var.get())

            # Update client in record manager
            self.record_manager.update_client(client)

            # Refresh client list
            self.load_clients()

            # Close the modal
            modal.destroy()

            messagebox.showinfo(
                "Success", f"Client {client.get_name()} updated successfully!")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to update client: {str(e)}")

    def delete_client(self):
        """Delete the selected client record."""
        # Check if a client is selected
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "Warning", "Please select a client to delete")
            return

        # Get the selected client
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, "values")

        try:
            client_id = int(values[0])
            client = self.record_manager.get_client(client_id)

            if client:
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"Are you sure you want to delete client "
                    f"{client.get_name()}?")

                if confirm:
                    # Delete client from record manager
                    self.record_manager.delete_client(client_id)

                    # Refresh client list
                    self.load_clients()

                    messagebox.showinfo(
                        "Success", "Client deleted successfully!")
        except ValueError as e:
            if "associated flights" in str(e):
                messagebox.showwarning(
                    "Cannot Delete",
                    f"Client '{client.get_name()}' has associated flights "
                    "and cannot be deleted. Please delete the flights first.")
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete client: {str(e)}")
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror(
                "Error", f"Failed to delete client: {str(e)}")

    def search_clients(self):
        """Search for clients based on the search term."""
        search_term = self.search_var.get()

        if not search_term:
            # If search term is empty, load all clients
            self.load_clients()
            return

        try:
            # Search clients by name, city, or country
            clients = self.record_manager.search_clients(search_term)

            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Add search results to treeview
            for client in clients:
                self.tree.insert("", "end", values=(
                    client.get_id(),
                    client.get_name(),
                    client.get_address_line_1(),
                    client.get_address_line_2(),
                    client.get_address_line_3(),
                    client.get_city(),
                    client.get_state(),
                    client.get_zip_code(),
                    client.get_country(),
                    client.get_phone_number()
                ))
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def load_clients(self):
        """Load all clients from the record manager into the treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all clients from record manager
        clients = []
        for record in self.record_manager.records:
            if record.get("Type") == "client":
                client = self.record_manager.get_client(record.get("ID"))
                clients.append(client)

        # Add clients to treeview
        for client in clients:
            self.tree.insert("", "end", values=(
                client.get_id(),
                client.get_name(),
                client.get_address_line_1(),
                client.get_address_line_2(),
                client.get_address_line_3(),
                client.get_city(),
                client.get_state(),
                client.get_zip_code(),
                client.get_country(),
                client.get_phone_number()
            ))

    def on_client_select(self, event):  # pylint: disable=W0613
        """Handle client selection in the treeview."""
        # Get selected items
        selected_items = self.tree.selection()

        # Check if any item is selected
        if not selected_items:
            return

        # Get the first selected item
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, "values")

        try:
            # Get client from record manager
            client = self.record_manager.get_client(int(values[0]))

            # Store the selected client for later use
            self.selected_client = client
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Error", f"Failed to select client: {str(e)}")

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
        """Clear the search field and reload all clients."""
        self.search_var.set("")
        self.load_clients()

    def is_placeholder(self, entry, placeholder):
        """Check if the entry contains placeholder text."""
        entry_text = entry.get().strip()
        entry_color = entry.cget('fg')

        # More robust color check
        is_grey = entry_color.lower() in [
            'grey', 'gray'] or entry_color == '#808080'

        # Case-insensitive comparison of text
        return entry_text.lower() == placeholder.lower() and is_grey

    def get_entry_value(self, entry, placeholder):
        """Get the actual value from an entry, ignoring placeholder text."""
        if self.is_placeholder(entry, placeholder):
            return ""
        return entry.get().strip()  # Strip whitespace from actual values
