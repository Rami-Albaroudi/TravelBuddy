# README

# CSCK541_GroupB - End of Module CSCK541 Assignment for Group B

### What is this project?

This repository contains a Python-based application/record management system for a travel agent. The system manages three types of records: Client records, Flight Records, and Airline Company records. It provides a Graphical User Interface (GUI) that allows users to create, delete, update, search, and display records. It stores data in a structured format for quick retrieval and modification.

**Key Features:**

- Create, delete, update, and search records for clients, flights, and airlines
- User-friendly graphical interface
- Data persistence using file system storage
- Robust error handling and data validation

---

### Record Formats

The program manages three types of records:

1. **Client Record:**

   - ID: int
   - Type: str (type of record)
   - Name: str
   - Address Line 1: str
   - Address Line 2: str
   - Address Line 3: str
   - City: str
   - State: str
   - Zip Code: str
   - Country: str
   - Phone Number: str

2. **Airline Record:**

   - ID: int
   - Type: str (type of record)
   - Company Name: str

3. **Flight Record:**
   - Client_ID: int
   - Airline_ID: int
   - Date: date/time
   - Start City: str
   - End City: str

---

### Data Storage

Records are stored internally as a list of dictionaries. The application saves data to the file system when closed and checks for existing records when started. Data is stored using JSONL (JSON Lines).

---

### Repository Structure

```
CSCK541_GroupB
├── docs                          # Documentation directory
│   ├── DirectoryTree.txt         # File containing the project's directory structure
│   ├── LICENCE                   # Licence file for the project
│   ├── README.md                 # Project readme file with overview and instructions
│   └── requirements.txt          # List of project dependencies
├── src                           # Source code directory
│   ├── .gitignore                # Git ignore file for specifying untracked files
│   ├── data                      # Data models and management
│   │   ├── airline.py            # Airline class definition
│   │   ├── client.py             # Client class definition
│   │   ├── flight.py             # Flight class definition
│   │   ├── record_manager.py     # RecordManager class for data operations
│   │   └── __init__.py           # Makes data a Python package
│   ├── gui                       # Graphical User Interface components
│   │   ├── airline_gui.py        # AirlineGUI class for airline record management
│   │   ├── client_gui.py         # ClientGUI class for client record management
│   │   ├── flight_gui.py         # FlightGUI class for flight record management
│   │   ├── gui.py                # Main GUI class (TravelAgentApp)
│   │   └── __init__.py           # Makes gui a Python package
│   ├── main.py                   # Entry point of the application
│   └── record                    # Directory for storing record data
│       └── record.jsonl          # JSONL file for persistent data storage
└── tests                         # Test directory
    ├── unit_tests.py             # Unit tests for the application
    └── __init__.py               # Makes tests a Python package
```

---

### How do I get set up?

#### 1. Clone the Repository

```
git clone
cd
```

#### 2. Set Up the Environment

**Anaconda/Miniconda** is required. Using **Anaconda/Miniconda**, create and activate a virtual environment:

```
conda create --name travel_agent_system python=3.x -y
conda activate travel_agent_system
```

#### 3. Install Dependencies

Install the required Python packages:

```
conda install --file requirements.txt
```

---

### Running the Application

First, to navigate to the main folder if it is not already selected, run

```
cd CSCK541_GroupB
```

To start the Travel Agent Record Management System, run:

```
python src/main.py
```

### Running Unit Tests

To run the program's unit tests, run:

```
python tests/unit_tests.py
```

---

### Navigation and Usage

The application supports the following interactions and keyboard shortcuts:

- **Double-click**: Select a record for update
- **Backspace**: Delete a selected record (with confirmation warning)
- **Enter**: Update a selected record
- **Enter** (in search box): Trigger the search function

All actions trigger appropriate modals:

- Create and Update actions open a form modal
- Delete actions display a warning confirmation
- Invalid inputs show warning messages

---

### Known Issues

1. Rapid clicks/inputs may result in errors or crash the program.
2. Excessively long strings or fields may produce visual glitches.
3. Large JSONL datasets may take a significant amount of time to load.
4. Invalid inputs might skip the validation process and cause errors.

---

### Who do I talk to?

For questions or issues, please contact:

- **Author**: Mirko Tagliaferri (Repo Owner)
- **Email**: m.tagliaferri@liverpool.ac.uk

### Authors

Leung Wong, Michael Scavera, Mirko Tagliaferri, and Rami Albaroudi.
