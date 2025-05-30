"""
Python file containing the Airline class and all the related methods.
"""


class Airline:
    """
    Airline class used to define airline instances.

    Airline Class Attributes:
    - id (int): unique identifier of an airline instance;
    - record_type (str): identifies an airline instance as an airline;
    - company_name (str): name of the airline being instantiated.

    Airline Class Methods:
    - __init__: assigning values to the properties of an Airline instance;
    - all relevant getters;
    - all relevant setters;
    - __str__: defining how an airline instance should appear when printed;
    - to_dict: transforming an airline instance into a dictionary;
    - from_dict: creating an airline instance from an appropriate dictionary.
    """

    def __init__(self, id_number=None, record_type="airline", company_name=""):
        """
        Instantiating an airline with the specified attributes.

        When the airline id is missing in the instantiation, a
        placeholder value of 0 is used to identify the instance.
        """
        self.record_type = record_type
        # Validate company name
        if company_name is not None:
            self.set_company_name(company_name)
        else:
            self.set_company_name("")

        # Validate ID if provided
        if id_number is not None:
            self.set_id(id_number)
        else:
            self.set_id(0)

    # Defining all the getter methods for the Airline class.
    def get_id(self):
        """
        Getter method retrieving an airline's id.
        """
        return self.id

    def get_record_type(self):
        """
        Getter method retrieving an airline's record type.
        """
        return self.record_type

    def get_company_name(self):
        """
        Getter method retrieving an airline's company name.
        """
        return self.company_name

    # Defining all the setter methods for the Airline class with basic validation
    def set_id(self, newid):
        """
        Setter method changing an airline's id.
        """
        if not isinstance(newid, int):  # Checks if newid is of the correct type
            raise TypeError("ID must be an integer")

        # Only validate the ID format if it's not the placeholder value
        if newid != 0:
            if str(newid)[0] != "9":  # Checks if newid starts with the proper type identifier
                raise ValueError("Airline IDs must start with a 9")
        self.id = newid

    def set_record_type(self, newtype="airline"):
        """
        Setter method changing an airline's record type.

        Although this setter function is useless in the
        current program, it allows for evolutions of the
        program where there are airlines of different type.
        For example, national or international airlines.
        """
        # Validate that type is "airline" for now.
        if newtype != "airline":
            raise ValueError("Record type must be 'airline'")
        self.record_type = newtype

    def set_company_name(self, new_company_name=""):
        """
        Setter method changing an airline's company name.
        """
        if not new_company_name:
            raise ValueError("Company name cannot be empty")
        self.company_name = new_company_name

    # Defining the __str__ method for the Airline class with better formatting
    def __str__(self):
        return f"Airline ID: {self.get_id()}\nCompany Name: {self.get_company_name()}"

    def to_dict(self):
        """
        Convert Airline object to dictionary for storage.
        The keys of the dictionary are chosen according
        to the requirements.
        """
        return {
            "ID": self.get_id(),
            "Type": self.get_record_type(),
            "Company Name": self.get_company_name()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates an Airline object starting from data
        extracted from a given dictionary.

        The method will be used when manipulating
        airlines' records after the import from the
        jsonline storage file.
        """
        return cls(
            id_number=data.get("ID"),
            record_type=data.get("Type", "airline"),
            company_name=data.get("Company Name", "")
        )
