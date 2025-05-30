"""
Principal python file containing the RecordManager class.
This module defines the main functionalities of the Record Management System.
"""

from datetime import datetime  # Imported to properly format dates.
import os  # Imported to properly handly file paths.
import random  # Imported to create random IDs for clients and airlines.
# Imported to manage the input/output to the record storage files.
import jsonlines
from .flight import Flight
from .client import Client
from .airline import Airline
# Get the project root directory to save the record.jsonl files
# to the correct folder.
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
default_file_path = os.path.join(project_root, "src", "record", "record.jsonl")


class RecordManager:
    """
    RecordManager class used to manage the records to and from the data storage files
    and to implement the CRUD functionalities (Create, Read, Update and Delete).

    RecordManager Class Attributes:
    - file_path (str): location of the data storage file.
    - records (list): list containing dictionaries. Each dictionary is a record.

    RecordManager Class Methods:
    - load_records: imports records from the data storage file into the records attribute.
    - save_records: saves records from the records attribute to the data storage file.
    - get_next_id: creates a new id for either a client or an airline record.
    - CRUD methods for client records.
    - CRUD methods for airline records.
    - CRUD methods for flight records.

    """

    def __init__(self, file_path=default_file_path):
        self.file_path = file_path
        self.records = []  # Initiates an empty list of records.
        # Uploads records from the file to the records list.
        self.load_records()

    def load_records(self):
        """Load records from JSONL file if it exists"""
        if os.path.exists(self.file_path):
            # Open the jsonl file in read mode.
            with jsonlines.open(self.file_path, 'r') as file:
                for line in file:
                    # Cycles through all records and uploads them to the records list.
                    self.records.append(line)
            # Closes the jsonl file once all records have been uploaded locally.
            file.close()
        else:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def save_records(self):
        """Save records to JSONL file"""
        with jsonlines.open(self.file_path, 'w') as file:  # Open the jsonl file in write mode.
            for record in self.records:  # Copies all records back into the jsonl file.
                file.write(record)
            # Closes the jsonl file once all records have been copied.
            file.close()

    def get_next_id(self, record_type):
        """
        Generate the next available integer ID for a given record type.
        It is assumed that a maximum of 100 billion IDs are allowed
        for each record type.

        The function extracts all the IDs currently employed by the
        management system. It then sets a type identifier:

        - integer 1 for clients' records;
        - integer 9 for airlines' records;

        The type identifier will prefix the IDs to allow a quick
        appropriateness check of the ID.

        A random integer ID is then generated and the type identifier
        is prefixed. If the ID create already exists, another random
        ID is generated.

        Args:
        - record_type (str) :   the type of the record for which the
                                ID has to be generated.

        Output:
        - random_id (int)   :   an integer ID whose prefix indicates
                                the type of record the ID identifies.
        """
        # Extracts all used IDs
        used_ids = []
        for record in self.records:
            used_ids.append(record.get("ID"))

        # Set type identifier for record type
        type_identifier = 0

        if record_type == "client":  # Sets the type_identifier to 1 for clients.
            type_identifier = 1
        elif record_type == "airline":  # Sets the type_identifier to 9 for airlines.
            type_identifier = 9

        # Creates a random_id of length 12, where the first digit identifies the type of record.
        random_id = int(str(type_identifier) +
                        str(random.randint(1, 99999999999)).rjust(11, "0"))

        # If the id is already used for another record, a new random id is created.
        # Even at 99% capacity (when 99 billion id have already been used), on average
        # the while loop will repeat for 64 times.
        while random_id in used_ids:
            random_id = int(str(type_identifier) +
                            str(random.randint(1, 99999999999)).rjust(11, "0"))

        return random_id

    # Client CRUD operations
    def create_client(self, client):
        """
        Add a new client record.

        Arg:
        - client (Client): a client object.

        Output:
        - client.get_id() (int): the client's id.

        Side effect:
        - The function adds the new client both to the records list and the jsonl file.
        """
        if not hasattr(client, 'to_dict'):  # Input validation.
            raise TypeError("The input must be a Client object")

        # Check if client with same ID already exists.
        # Alhtough not strictly needed, this ensures that if the get_new_id method is changed,
        # the data storage file will not contain repeated entries.
        for record in self.records:
            if record.get("Type") == "client" and record.get("ID") == client.get_id():
                raise ValueError(
                    f"Client with ID {client.get_id()} already exists")

        # Add the client record
        self.records.append(client.to_dict())
        self.save_records()
        return client.get_id()

    def get_client(self, client_id):
        """
        Retrieve a client record by ID.

        Arg:
        - client_id (int): the client's ID.

        Output:
        - The client record (Client) corresponding to the ID if it exists.
        - None (None) if there are no clients with the provided ID.
        """
        for record in self.records:  # Cycles through all records to find correspondence.
            if record.get("Type") == "client" and record.get("ID") == client_id:
                return Client.from_dict(record)
        return None

    def update_client(self, client):
        """
        Update an existing client record.

        Arg:
        - client (Client): a client object.

        Output:
        - True (bool) if the update was successful.
        - False (bool) if the update was unsuccessful.

        Side effect:
        - The record is, possibly, updated with the new values.
        """
        if not hasattr(client, 'to_dict'):  # Input validation.
            raise TypeError("The input must be a Client object")

        # Identifies the position of the record to update.
        for i, record in enumerate(self.records):
            if record.get("Type") == "client" and record.get("ID") == client.get_id():
                # Updates the record with the new data.
                self.records[i] = client.to_dict()
                self.save_records()  # Saves the record.
                return True
        return False

    def delete_client(self, client_id):
        """
        Delete a client record by ID.
        If the client has booked flights, the deletion is blocked.

        Arg:
        - client_id (int): the id of the client to be deleted.

        Output:
        - True (bool) if the deletion was successful.
        - False (bool) if the deletion was unsuccessful.

        Side effect:
        - The record is, possibly, deleted.
        """
        for i, record in enumerate(self.records):
            if record.get("Type") == "client" and record.get("ID") == client_id:
                # Check if there are any flights associated with this client
                for flight_record in self.records:
                    if "Client_ID" in flight_record and flight_record.get("Client_ID") == client_id:
                        raise ValueError(
                            f"Cannot delete client with ID {client_id} "
                            f"as it has associated flights")

                del self.records[i]
                self.save_records()
                return True
        return False

    def search_clients(self, search_term):
        """
        Search for clients by any field using partial matching.

        Arg:
        - search_term (str): search key.

        Output:
        - results (list): a list of records corresponding with the search key.
        """
        results = []  # Initialize empty list of results

        # Format the search term to lowercase for case-insensitive matching
        search_term_lower = search_term.lower()

        for record in self.records:
            if record.get("Type") == "client":
                # Try to match the search term against any field
                if any(
                    search_term_lower in str(value).lower()
                    for key, value in record.items()
                    if key != "Type" and value is not None
                ):
                    results.append(Client.from_dict(record))

        return results

    # Airline CRUD operations
    def create_airline(self, airline):
        """
        Add a new airline record.

        Arg:
        - airline (Airline): an airline object.

        Output:
        - airline.get_id() (int): the airline's id.

        Side effect:
        - The function adds the new airline both to the records list and the jsonl file.
        """
        if not hasattr(airline, 'to_dict'):  # Input validation.
            raise TypeError("The input must be an Airline object")

        # Check if airline with same ID already exists
        # Alhtough not strictly needed, this ensures that if the get_new_id method is changed,
        # the data storage file will not contain repeated entries.
        for record in self.records:
            if record.get("Type") == "airline" and record.get("ID") == airline.get_id():
                raise ValueError(
                    f"Airline with ID {airline.get_id()} already exists")

        # Add the airline record
        self.records.append(airline.to_dict())
        self.save_records()
        return airline.get_id()

    def get_airline(self, airline_id):
        """
        Retrieve an airline record by ID.

        Arg:
        - airline_id (int): the airline's ID.

        Output:
        - The airline record (Airline) corresponding to the ID if it exists.
        - None (None) if there are no airlines with the provided ID.
        """
        for record in self.records:  # Cycles through all records to check correspondence.
            if record.get("Type") == "airline" and record.get("ID") == airline_id:
                return Airline.from_dict(record)
        return None

    def update_airline(self, airline):
        """
        Update an existing airline record.

        Arg:
        - airline (Airline): an airline object.

        Output:
        - True (bool) if the update was successful.
        - False (bool) if the update was unsuccessful.

        Side effect:
        - The record is, possibly, updated with the new values.
        """
        if not hasattr(airline, 'to_dict'):  # Input validation
            raise TypeError("The input must be an Airline object")

        # Identifies the position of the record to update.
        for i, record in enumerate(self.records):
            if record.get("Type") == "airline" and record.get("ID") == airline.get_id():
                self.records[i] = airline.to_dict()  # Updates the record.
                self.save_records()  # Saves the record.
                return True
        return False

    def delete_airline(self, airline_id):
        """
        Delete an airline record by ID.
        If the airline has booked flights, the deletion is blocked.

        Arg:
        - airline_id (int): the id of the airline to be deleted.

        Output:
        - True (bool) if the deletion was successful.
        - False (bool) if the deletion was unsuccessful.

        Side effect:
        - The record is, possibly, deleted.
        """
        for i, record in enumerate(self.records):
            if record.get("Type") == "airline" and record.get("ID") == airline_id:
                # Check if there are any flights associated with this airline
                for flight_record in self.records:
                    if "Airline_ID" in flight_record and \
                            flight_record.get("Airline_ID") == airline_id:
                        raise ValueError(
                            f"Cannot delete airline with ID {airline_id} "
                            f"as it has associated flights")

                del self.records[i]
                self.save_records()
                return True
        return False

    def search_airlines(self, search_term):
        """
        Search for airlines by company name or ID.

        Arg:
        - search_term (str): search key.

        Output:
        - results (list): a list of records corresponding with the search key.
        """
        results = []  # Initialised empty list of results.

        # Format the search term to lowercase for case-insensitive matching
        search_term_lower = search_term.lower()

        for record in self.records:
            if record.get("Type") == "airline":
                # Search by company name (case-insensitive)
                if search_term_lower in record.get("Company Name", "").lower():
                    results.append(Airline.from_dict(record))
                # Search by ID (including partial matches)
                elif search_term in str(record.get("ID", "")):
                    results.append(Airline.from_dict(record))

        return results

    # Flight CRUD operations
    def create_flight(self, flight):
        """Add a new flight record.

        Arg:
        - flight (Flight): a flight object.

        Output:
        - A tuple containing the client_id (int), the airline_id (int) and the date.
        """
        if not hasattr(flight, 'to_dict'):  # Input validation.
            raise TypeError("The input must be a Flight object")

        # Verify that the client and airline exist
        client_exists = False  # Client check flag.
        airline_exists = False  # Airline check flag.

        for record in self.records:
            if record.get("Type") == "client" and record.get("ID") == flight.get_client_id():
                client_exists = True  # If client exists, updates flag to True.
            if record.get("Type") == "airline" and record.get("ID") == flight.get_airline_id():
                # If airline exists, updates flag to True.
                airline_exists = True

        if not client_exists:  # Validation over clients.
            raise ValueError(
                f"Client with ID {flight.get_client_id()} does not exist")
        if not airline_exists:  # Validation over airlines.
            raise ValueError(
                f"Airline with ID {flight.get_airline_id()} does not exist")

        # Add the flight record
        self.records.append(flight.to_dict())
        self.save_records()
        # Return a tuple of the composite key instead of an ID
        return (flight.get_client_id(), flight.get_airline_id(), flight.get_date())

    def get_flight(self, client_id, airline_id, date=None):
        """Retrieve a flight record by client_id and airline_id.

        Args:
        - client_id (int): the client's identifier.
        - airline_id (int): the airline's identifier.
        - [date] (str): the date of the flight.

        Output:
        - The flight (Flight) corresponding to the input data, if it exists.
        - None (None) if no flight exists with the given data.
        """
        for record in self.records:
            if (record.get("Type") == "flight" and
                record.get("Client_ID") == client_id and
                    record.get("Airline_ID") == airline_id):
                # If date is provided, check it too
                if date is None or record.get("Date") == date:
                    return Flight.from_dict(record)
        return None

    def get_flights_by_client(self, client_id):
        """
        Retrieve all flights for a specific client.

        Arg:
        - client_id (int): the client's identifier.

        Output:
        - results (list): a list of the flights for that specific client.
        """
        results = []  # Initiates empty list of results.
        for record in self.records:
            if record.get("Type") == "flight" and record.get("Client_ID") == client_id:
                # Appends all flights for the given client.
                results.append(Flight.from_dict(record))
        return results

    def get_flights_by_airline(self, airline_id):
        """
        Retrieve all flights for a specific airline.

        Arg:
        - airline_id (int): the airline's identifier.

        Output:
        - results (list): a list of the flights for that specific airline.
        """
        results = []  # Initiates empty list of results.
        for record in self.records:
            if record.get("Type") == "flight" and record.get("Airline_ID") == airline_id:
                # Appends all flights for the given airline.
                results.append(Flight.from_dict(record))
        return results

    def update_flight(self, flight, client_id, airline_id, date):
        """
        Update an existing flight record.

        Args:
        - flight (Flight): A flight object with updated values.
        - client_id (int): The original client ID of the flight.
        - airline_id (int): The original airline ID of the flight.
        - date: The original date of the flight.

        Returns:
        - True (bool): If the update was successful.
        - False (bool): If the update was unsuccessful.
        """
        if not hasattr(flight, 'to_dict'):  # Input validation.
            raise TypeError("The input must be a Flight object")

        # Convert date to string format if it's a datetime object
        date_str = date.isoformat() if isinstance(date, datetime) else date

        # Identifies the position of the flight record.
        for i, record in enumerate(self.records):
            if (record.get("Type") == "flight" and
                record.get("Client_ID") == client_id and
                record.get("Airline_ID") == airline_id and
                    str(record.get("Date")) == str(date_str)):
                self.records[i] = flight.to_dict()  # Updates the record.
                self.save_records()  # Saves the record.
                return True
        return False

    def delete_flight(self, client_id, airline_id, date=None):
        """
        Delete a flight record by client_id and airline_id.

        Args:
        - client_id (int): the client's identifier.
        - airline_id (int): the airline's identifier.
        - [date] (str): the date of the flight.

        Output:
        - True (bool) if the update was successful.
        - False (bool) if the update was unsuccessful.

        Side effect:
        - The record is, possibly, updated with the new values.
        """
        for i, record in enumerate(self.records):  # Identifies the position of the record.
            if (record.get("Type") == "flight" and
                record.get("Client_ID") == client_id and
                    record.get("Airline_ID") == airline_id):
                # If date is provided, check it too
                if date is None or record.get("Date") == date:
                    del self.records[i]  # Deletes the record.
                    self.save_records()  # Updates the data storage file.
                    return True
        return False

    def search_flights(self, start_city=None, end_city=None, date=None,
                       client_id=None, airline_id=None):
        """
        Search for flights by start city, end city, date, client ID, or airline ID.

        Args:
        - [start_city] (str): departure city search key.
        - [end_city] (str): arrival city search key.
        - [date] (str or datetime): date search key.
        - [client_id] (int): client ID search key.
        - [airline_id] (int): airline ID search key.

        Output:
        - results (list): a list of Flight objects corresponding with the search key(s).
        """
        results = []

        for record in self.records:
            if record.get("Type") == "flight":
                match = True  # Flag checking for input validation.

                if start_city and start_city.lower() not in record.get("Start City", "").lower():
                    match = False
                if end_city and end_city.lower() not in record.get("End City", "").lower():
                    match = False
                if date:
                    record_date = record.get("Date")
                    if isinstance(date, str) and record_date != date:
                        match = False
                    elif isinstance(date, datetime):
                        try:
                            record_datetime = datetime.fromisoformat(
                                record_date)
                            if record_datetime.date() != date.date():
                                match = False
                        except (ValueError, TypeError):
                            match = False
                if client_id and record.get("Client_ID") != client_id:
                    match = False
                if airline_id and record.get("Airline_ID") != airline_id:
                    match = False

                if match:
                    results.append(Flight.from_dict(record))

        return results
