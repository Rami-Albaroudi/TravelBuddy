"""
Python file containing the Flight class and all the related methods.
"""
from datetime import datetime  # Imported to properly format date elements in flight instances.


class Flight:
    """
    Flight class used to define flight instances.

    Flight Class Attributes:
    - client_id (int): identifier of the client who booked the flight;
    - airline_id (int): identifier of the airline who will provide the flight;
    - date (date): date of the flight;
    - start_city (str): city from which the flight departs;
    - end_city (str): city where the flight arrives;
    - record_type (str): indication of the record_type.

    Flight Class Methods:
    - __init__: assigning values to the properties of a Flight instance, with basic validation;
    - all relevant getters;
    - all relevant setters;
    - __str__: defining how a flight instance should appear when printed;
    - to_dict: transforming a flight instance into a dictionary;
    - from_dict: creating a flight instance from an appropriate dictionary.
    """

    def __init__(self, client_id, airline_id, date, start_city="", end_city="",
                 record_type="flight"):
        """
        Instantiating a flight with the specified attributes.

        Basic validation is performed on the client_id and airline_id attributes.
        The date attribute is converted to the proper format if needed.
        """
        self.set_record_type(record_type)
        self.set_client_id(client_id)
        self.set_airline_id(airline_id)
        self.set_date(date)
        self.set_start_city(start_city)
        self.set_end_city(end_city)

    # Defining all the getter methods for the Flight class.
    def get_record_type(self):
        """
        Getter method retrieving a flight's record type.
        """
        return self.record_type

    def get_client_id(self):
        """
        Getter method retrieving the client's id of a flight.
        """
        return self.client_id

    def get_airline_id(self):
        """
        Getter method retrieving the airline's id of a flight.
        """
        return self.airline_id

    def get_date(self):
        """
        Getter method retrieving a flight's date.
        """
        return self.date

    def get_start_city(self):
        """
        Getter method retrieving a flight's departure city.
        """
        return self.start_city

    def get_end_city(self):
        """
        Getter method retrieving a flight's arrival city.
        """
        return self.end_city

    # Defining all the setter methods for the Flight class with basic validation.
    def set_client_id(self, new_client_id):
        """
        Setter method changing the client's id of a flight.
        """
        if not isinstance(new_client_id, int):  # Checks if new_client_id is of the correct type.
            raise TypeError("Client ID must be an integer")

        # Checks if newid starts with the proper type identifier
        if str(new_client_id)[0] != "1":
            raise ValueError("Clients' IDs must start with a 1")
        self.client_id = new_client_id

    def set_record_type(self, newtype="flight"):
        """
        Setter method changing a flight's record type.

        Although this setter function is useless in the
        current program, it allows for evolutions of the
        program where there are flights of different type.
        For example, special flights for an airline.
        """
        # Validate that type is "flight" for now.
        if newtype != "flight":
            raise ValueError("Record type must be 'flight'")
        self.record_type = newtype

    def set_airline_id(self, new_airline_id):
        """
        Setter method changing the airline's id of a flight.
        """
        if not isinstance(new_airline_id, int):  # Checks if new_airline_id is of the correct type.
            raise TypeError("Airline ID must be an integer")

        # Checks if new_airline_id is in proper format.
        if str(new_airline_id)[0] != "9":
            raise ValueError("Airlines' IDs must start with a 9")
        self.airline_id = new_airline_id

    def set_date(self, new_date):
        """
        Setter method changing the flight's date.

        The method also converts dates given as strings into
        an appropriate date format.
        """
        if isinstance(new_date, str):  # Checks whether the date is a string.
            try:  # Tries to convert the date to a date format if the string compliant with ISO8601.
                self.date = datetime.fromisoformat(new_date)
            except ValueError:
                try:  # Tries to adjusts the date given as a string to an appropriate format.
                    self.date = datetime.strptime(
                        new_date, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:  # Tries to adjusts the date given as a string to an appropriate format.
                        self.date = datetime.strptime(new_date, "%Y-%m-%d")
                    except ValueError as ex:  # If no adjustments are possible, raises an error.
                        raise ValueError(
                            "Invalid date format. Use YYYY-MM-DD HH:MM:SS, or YYYY-MM-DD.") from ex
        # If in the correct format, set date.
        elif isinstance(new_date, datetime):
            self.date = new_date
        else:  # If date is neither in string nor in date format, raise an error.
            raise TypeError("Date must be a string or datetime object")

    def set_start_city(self, new_start_city):
        """
        Setter method changing a flight's departure city.
        """
        if not new_start_city:
            raise ValueError("Start city cannot be empty")
        self.start_city = new_start_city

    def set_end_city(self, new_end_city):
        """
        Setter method changing a flight's arrival city.
        """
        if not new_end_city:
            raise ValueError("End city cannot be empty")
        self.end_city = new_end_city

    # Defining the __str__ method for the Flight class with better formatting
    def __str__(self):
        return (f"Client ID: {self.get_client_id()}, Airline ID: {self.get_airline_id()}\n"
                f"Date: {self.get_date().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Route: {self.get_start_city()} to {self.get_end_city()}")

    def to_dict(self):
        """
        Convert Flight object to dictionary for storage.
        The keys of the dictionary are chosen according
        to the requirements.

        Date attributes are converted back to string formats
        for storage.
        """
        # Date conversion from date format to string format.
        date_str = self.get_date().isoformat() if isinstance(
            self.get_date(), datetime) else self.get_date()
        return {
            "Type": self.get_record_type(),
            "Client_ID": self.get_client_id(),
            "Airline_ID": self.get_airline_id(),
            "Date": date_str,
            "Start City": self.get_start_city(),
            "End City": self.get_end_city()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a flight object starting from data
        extracted from a given dictionary.

        The method will be used when manipulating
        flights' records after the import from the
        jsonline storage file.
        """
        return cls(
            client_id=data.get("Client_ID"),
            airline_id=data.get("Airline_ID"),
            date=data.get("Date"),
            start_city=data.get("Start City", ""),
            end_city=data.get("End City", ""),
            record_type=data.get("Type", "flight")
        )
