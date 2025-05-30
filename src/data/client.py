"""
Python file containing the Client class and all the related methods.
"""


class Client:
    """
    Client class used to define client instances.

    Client Class Attributes:
    - id (int): unique identifier of a client instance;
    - record_type (str): identifies a client instance as a client;
    - name (str): name of the client being instantiated;
    - address_line_1 (str): street/square of client's address;
    - address_line_2 (str): civic number of the client's address;
    - address_line_3 (str): apartment/suite/unit identification;
    - city (str): city where the client lives;
    - state (str): state/region where the client lives;
    - zip_code (str): zip/postal code;
    - country (str): country where the client lives;
    - phone_number (str): client's phone number.

    Client Class Methods:
    - __init__: assigning values to the properties of a Client instance;
    - all relevant getters;
    - all relevant setters;
    - __str__: defining how a client instance should appear when printed;
    - to_dict: transforming a client instance into a dictionary;
    - from_dict: creating a client instance from an appropriate dictionary.
    """

    def __init__(self, id_number=None, record_type="client", name="", address_line_1="",
                 address_line_2="", address_line_3="", city="", state="",
                 zip_code="", country="", phone_number=""):
        """
        Instantiating a client with the specified attributes.

        When the client id is missing in the instantiation, a
        placeholder value of 0 is used to identify the instance.
        """
        self.set_id(id_number if id_number is not None else 0)
        self.set_record_type(record_type)
        self.set_name(name)
        self.set_address_line_1(address_line_1)
        self.set_address_line_2(address_line_2)
        self.set_address_line_3(address_line_3)
        self.set_city(city)
        self.set_state(state)
        self.set_zip_code(zip_code)
        self.set_country(country)
        self.set_phone_number(phone_number)

    # Defining all the getter methods for the Client class.
    def get_id(self):
        """
        Getter method retrieving a client's id.
        """
        return self.id

    def get_record_type(self):
        """
        Getter method retrieving a client's record_type.
        """
        return self.record_type

    def get_name(self):
        """
        Getter method retrieving a client's name.
        """
        return self.name

    def get_address_line_1(self):
        """
        Getter method retrieving a client's street/square
        indication of the address.
        """
        return self.address_line_1

    def get_address_line_2(self):
        """
        Getter method retrieving a client's civic number
        indication of the address.
        """
        return self.address_line_2

    def get_address_line_3(self):
        """
        Getter method retrieving a client's apartment
        suite/unit indication of the address.
        """
        return self.address_line_3

    def get_full_address(self):
        """
        Getter method retrieving a client's full address.
        """
        # Only include non-empty address lines with proper formatting
        address_parts = []
        if self.address_line_1:
            address_parts.append(self.address_line_1)
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        if self.address_line_3:
            address_parts.append(self.address_line_3)

        return ", ".join(address_parts)

    def get_city(self):
        """
        Getter method retrieving a client's city.
        """
        return self.city

    def get_state(self):
        """
        Getter method retrieving a client's state/region.
        """
        return self.state

    def get_zip_code(self):
        """
        Getter method retrieving a client's zip/postal
        code.
        """
        return self.zip_code

    def get_country(self):
        """
        Getter method retrieving a client's country.
        """
        return self.country

    def get_phone_number(self):
        """
        Getter method retrieving a client's phone number.
        """
        return self.phone_number

    # Defining all the setter methods for the Client class with basic validation
    def set_id(self, newid):
        """
        Setter method changing a client's id.
        """
        if not isinstance(newid, int):  # Checks if newid is of the correct type
            raise TypeError("ID must be an integer")

        # Checks if newid starts with the proper type identifier
        if newid != 0 and str(newid)[0] != "1":
            raise ValueError("Client IDs must start with a 1")
        self.id = newid

    def set_record_type(self, newtype="client"):
        """
        Setter method changing a client's record type.

        Although this setter function is useless in the
        current program, it allows for evolutions of the
        program where there are clients of different type.
        For example, clients with special status for an airline.
        """
        # Validate that type is "client" for now.
        if newtype != "client":
            raise ValueError("Record type must be 'client'")
        self.record_type = newtype

    def set_name(self, newname=""):
        """
        Setter method changing a client's name.
        """
        if not newname:
            raise ValueError("Name cannot be empty")
        self.name = newname

    def set_address_line_1(self, new_address_line_1=""):
        """
        Setter method changing a client's street/square
        indication of the address.
        """
        self.address_line_1 = new_address_line_1

    def set_address_line_2(self, new_address_line_2=""):
        """
        Setter method changing a client's civic number
        indication of the address.
        """
        self.address_line_2 = new_address_line_2

    def set_address_line_3(self, new_address_line_3=""):
        """
        Setter method changing a client's apartment
        suite/unit indication of the address.
        """
        self.address_line_3 = new_address_line_3

    def set_city(self, newcity=""):
        """
        Setter method changing a client's city.
        """
        self.city = newcity

    def set_state(self, newstate=""):
        """
        Setter method changing a client's state/region.
        """
        self.state = newstate

    def set_zip_code(self, newzip=""):
        """
        Setter method changing a client's zip/postal code.
        """
        self.zip_code = newzip

    def set_country(self, newcountry=""):
        """
        Setter method changing a client's country.
        """
        self.country = newcountry

    def set_phone_number(self, newphone=""):
        """
        Setter method changing a client's phone number.
        """
        self.phone_number = newphone

    # Defining the __str__ method for the Client class with better formatting
    def __str__(self):
        return (f"Client ID: {self.get_id()}\n"
                f"Name: {self.get_name()}\n"
                f"Address: {self.get_full_address()}\n"
                f"City: {self.get_city()}\n"
                f"State or Region: {self.get_state()}\n"
                f"Postal or Zip: {self.get_zip_code()}\n"
                f"Country: {self.get_country()}\n"
                f"Phone number: {self.get_phone_number()}")

    def to_dict(self):
        """
        Convert Client object to dictionary for storage.
        The keys of the dictionary are chosen according
        to requirements.
        """
        return {
            "ID": self.get_id(),
            "Type": self.get_record_type(),
            "Name": self.get_name(),
            "Address Line 1": self.get_address_line_1(),
            "Address Line 2": self.get_address_line_2(),
            "Address Line 3": self.get_address_line_3(),
            "City": self.get_city(),
            "State": self.get_state(),
            "Zip Code": self.get_zip_code(),
            "Country": self.get_country(),
            "Phone Number": self.get_phone_number()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Client object starting from data
        extracted from a given dictionary.

        The method will be used when manipulating
        clients' records after the import from the
        jsonline storage file.
        """
        return cls(
            id_number=data.get("ID"),
            record_type=data.get("Type", "client"),
            name=data.get("Name", ""),
            address_line_1=data.get("Address Line 1", ""),
            address_line_2=data.get("Address Line 2", ""),
            address_line_3=data.get("Address Line 3", ""),
            city=data.get("City", ""),
            state=data.get("State", ""),
            zip_code=data.get("Zip Code", ""),
            country=data.get("Country", ""),
            phone_number=data.get("Phone Number", "")
        )
