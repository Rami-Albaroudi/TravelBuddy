"""
This module contains tests for Create, Read, Update, Delete (CRUD) operations
and search functionality for clients, airlines, and flights. The tests use
temporary files to avoid affecting production data.
"""

# Imports
import unittest
import tempfile
import sys
import os
from datetime import datetime
# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project root to Python path
sys.path.append(project_root)
from src.data.record_manager import RecordManager  # pylint: disable=C0413
from src.data.flight import Flight  # pylint: disable=C0413
from src.data.client import Client  # pylint: disable=C0413
from src.data.airline import Airline  # pylint: disable=C0413


# Unit tests for CRUD and search methods
class TestRecordManagerCRUDAndSearch(unittest.TestCase):
    """
    Tests for RecordManager's CRUD and search operations.

    Tests the functionality of RecordManager including:
    - Client record operations (create, read, update, delete, search)
    - Airline record operations (create, read, update, delete, search)
    - Flight record operations (create, read, update, delete, search)
    - Record dependency handling

    Each test uses a temporary file for isolation.
    """

    def setUp(self):
        """
        Set up the test environment before each test. 
        Creates a temporary JSONL file and initializes a RecordManager
        instance with this file path.
        """
        # Create a temporary file to store the test records
        self.temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix='.jsonl')
        file_path = self.temp_file.name
        self.rm = RecordManager(file_path)

    def tearDown(self):
        """
        Clean up the test environment after each test. 
        Closes and removes the temporary file created in setUp.
        """
        # Close and delete the temporary file
        self.temp_file.close()
        os.unlink(self.temp_file.name)

    # Client Tests

    def test_create_client(self):
        """Test client creation, retrieval, and duplicate prevention."""
        # Get next available client ID
        next_id = self.rm.get_next_id("client")

        # Create a new client
        client = Client(next_id, "client", "John", "123 St",
                        "", "", "London", "LONDON", "10001", "UK")
        client_id = self.rm.create_client(client)

        # Test client creation
        self.assertEqual(client_id, next_id,
                         "Client ID should match the next available ID")

        # Test client retrieval
        retrieved = self.rm.get_client(next_id)
        self.assertIsNotNone(retrieved, "Retrieved client should not be None")
        self.assertEqual(retrieved.get_name(), "John",
                         "Retrieved client name should match")

        # Test duplicate client creation prevention
        with self.assertRaises(ValueError):
            self.rm.create_client(client)

    def test_get_client(self):
        """Test client retrieval and handling of non-existent clients."""
        # Create a test client
        client = Client(1, "client", "Jane", "456 St", "",
                        "", "Liverpool", "LP", "90001", "UK")
        self.rm.create_client(client)

        # Test retrieval of existing client
        retrieved = self.rm.get_client(1)
        self.assertIsNotNone(retrieved, "Retrieved client should not be None")
        self.assertEqual(retrieved.get_name(), "Jane",
                         "Retrieved client name should match")

        # Test retrieval of non-existent client
        non_existent = self.rm.get_client(199)
        self.assertIsNone(
            non_existent, "Non-existent client should return None")

    def test_update_client(self):
        """Test client update functionality and handling of non-existent clients."""
        # Create a test client
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        self.rm.create_client(client)

        # Update the client data
        updated_client = Client(
            1, "client", "John Doe", "123 St", "", "", "London", "LONDON", "10001", "UK")

        # Test successful update
        success = self.rm.update_client(updated_client)
        self.assertTrue(
            success, "Update should return True for existing client")

        # Verify client was updated correctly
        retrieved = self.rm.get_client(1)
        self.assertEqual(retrieved.get_name(), "John Doe",
                         "Client name should be updated")

        # Test update of non-existent client
        non_existent_update = self.rm.update_client(
            Client(199, "client", "Nonexistent"))
        self.assertFalse(non_existent_update,
                         "Update should return False for non-existent client")

    def test_delete_client(self):
        """Test client deletion and handling of non-existent clients."""
        # Create a test client
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        self.rm.create_client(client)

        # Test successful deletion
        success = self.rm.delete_client(1)
        self.assertTrue(
            success, "Deletion should return True for existing client")

        # Verify client was deleted
        retrieved = self.rm.get_client(1)
        self.assertIsNone(
            retrieved, "Client should no longer exist after deletion")

        # Test deletion of non-existent client
        non_existent_deletion = self.rm.delete_client(199)
        self.assertFalse(non_existent_deletion,
                         "Deletion should return False for non-existent client")

    def test_delete_client_with_flights(self):
        """Test client deletion when associated with flights and proper deletion sequence."""
        # Create test client, airline, and flight
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_client(client)
        self.rm.create_airline(airline)
        flight = Flight(1, 9, "2025-01-01", "London", "LP")
        self.rm.create_flight(flight)

        # Verify client with flights cannot be deleted directly
        with self.assertRaises(ValueError):
            self.rm.delete_client(1)

        # Delete the flight first
        self.rm.delete_flight(1, 9, flight.get_date().isoformat())

        # Now client deletion should succeed
        success = self.rm.delete_client(1)
        self.assertTrue(
            success, "Client deletion should succeed after flight is removed")

    def test_search_clients(self):
        """Test client search functionality with various search criteria."""
        # Create test clients
        client1 = Client(1, "client", "John", "123 St", "",
                         "", "London", "LONDON", "10001", "UK")
        client2 = Client(11, "client", "Jane", "456 St", "",
                         "", "Liverpool", "LP", "90001", "UK")
        self.rm.create_client(client1)
        self.rm.create_client(client2)

        # Test search by client name
        results = self.rm.search_clients("John")
        self.assertEqual(
            len(results), 1, "Should find exactly one client matching 'John'")
        self.assertEqual(results[0].get_name(), "John",
                         "Found client should have name 'John'")

        # Test search by city
        results = self.rm.search_clients("London")
        self.assertEqual(
            len(results), 1, "Should find exactly one client in London")

        # Test search by country
        results = self.rm.search_clients("UK")
        self.assertEqual(len(results), 2, "Should find both clients in the UK")

        # Test search with no matches
        results = self.rm.search_clients("Nonexistent")
        self.assertEqual(
            len(results), 0, "Should find no clients with non-existent criteria")

    # Airline Tests

    def test_create_airline(self):
        """Test airline creation, retrieval, and duplicate prevention."""
        # Get next available airline ID
        next_id = self.rm.get_next_id("airline")

        # Create a new airline
        airline = Airline(next_id, "airline", "AirCo")
        airline_id = self.rm.create_airline(airline)

        # Test airline creation
        self.assertEqual(airline_id, next_id,
                         "Airline ID should match the next available ID")

        # Test airline retrieval
        retrieved = self.rm.get_airline(next_id)
        self.assertIsNotNone(retrieved, "Retrieved airline should not be None")
        self.assertEqual(retrieved.get_company_name(),
                         "AirCo", "Company name should match")

        # Test duplicate airline creation prevention
        with self.assertRaises(ValueError):
            self.rm.create_airline(airline)

    def test_get_airline(self):
        """Test airline retrieval and handling of non-existent airlines."""
        # Create a test airline
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_airline(airline)

        # Test retrieval of existing airline
        retrieved = self.rm.get_airline(9)
        self.assertIsNotNone(retrieved, "Retrieved airline should not be None")
        self.assertEqual(retrieved.get_company_name(),
                         "AirCo", "Company name should match")

        # Test retrieval of non-existent airline
        non_existent = self.rm.get_airline(999)
        self.assertIsNone(
            non_existent, "Non-existent airline should return None")

    def test_update_airline(self):
        """Test airline update functionality and handling of non-existent airlines."""
        # Create a test airline
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_airline(airline)

        # Update the airline
        updated_airline = Airline(9, "airline", "NewAir")
        success = self.rm.update_airline(updated_airline)

        # Verify update was successful
        self.assertTrue(
            success, "Update should return True for existing airline")
        retrieved = self.rm.get_airline(9)
        self.assertEqual(retrieved.get_company_name(),
                         "NewAir", "Company name should be updated")

        # Test update of non-existent airline
        non_existent_update = self.rm.update_airline(
            Airline(999, "airline", "Nonexistent"))
        self.assertFalse(non_existent_update,
                         "Update should return False for non-existent airline")

    def test_delete_airline(self):
        """Test airline deletion and handling of non-existent airlines."""
        # Create a test airline
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_airline(airline)

        # Test successful deletion
        success = self.rm.delete_airline(9)
        self.assertTrue(
            success, "Deletion should return True for existing airline")

        # Verify airline was deleted
        retrieved = self.rm.get_airline(9)
        self.assertIsNone(
            retrieved, "Airline should no longer exist after deletion")

        # Test deletion of non-existent airline
        non_existent_deletion = self.rm.delete_airline(99)
        self.assertFalse(non_existent_deletion,
                         "Deletion should return False for non-existent airline")

    def test_delete_airline_with_flights(self):
        """Test airline deletion when associated with flights and proper deletion sequence."""
        # Create test client, airline, and flight
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_client(client)
        self.rm.create_airline(airline)
        flight = Flight(1, 9, "2025-01-01", "London", "LP")
        self.rm.create_flight(flight)

        # Verify airline with flights cannot be deleted directly
        with self.assertRaises(ValueError):
            self.rm.delete_airline(9)

        # Delete the flight first
        self.rm.delete_flight(1, 9, flight.get_date().isoformat())

        # Now airline deletion should succeed
        success = self.rm.delete_airline(9)
        self.assertTrue(
            success, "Airline deletion should succeed after flight is removed")

    def test_search_airlines(self):
        """Test airline search functionality with various search criteria."""
        # Create test airlines
        airline1 = Airline(9, "airline", "AirCo")
        airline2 = Airline(91, "airline", "CX")
        self.rm.create_airline(airline1)
        self.rm.create_airline(airline2)

        # Test search by exact airline name
        results = self.rm.search_airlines("AirCo")
        self.assertEqual(
            len(results), 1, "Should find exactly one airline matching 'AirCo'")
        self.assertEqual(results[0].get_company_name(
        ), "AirCo", "Found airline should have name 'AirCo'")

        # Test search by partial keyword
        results = self.rm.search_airlines("X")
        self.assertEqual(
            len(results), 1, "Should find exactly one airline containing 'X'")
        self.assertEqual(results[0].get_company_name(),
                         "CX", "Found airline should have name 'CX'")

        # Test search with no matches
        results = self.rm.search_airlines("Nonexistent")
        self.assertEqual(
            len(results), 0, "Should find no airlines with non-existent name")

    # Flight Tests

    def test_create_flight(self):
        """Test flight creation and retrieval functionality."""
        # Create test client and airline
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_client(client)
        self.rm.create_airline(airline)

        # Create a flight
        flight = Flight(1, 9, "2025-01-01", "London", "LP")
        key = self.rm.create_flight(flight)

        # Test flight creation
        expected_key = (1, 9, flight.get_date())
        self.assertEqual(key, expected_key,
                         "Flight key should match expected format")

        # Test flight retrieval
        retrieved = self.rm.get_flight(1, 9)
        self.assertIsNotNone(retrieved, "Retrieved flight should not be None")
        self.assertEqual(retrieved.get_start_city(),
                         "London", "Start city should match")

    def test_get_flight(self):
        """Test flight retrieval functionality."""
        # Create test client, airline, and flight
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_client(client)
        self.rm.create_airline(airline)
        flight = Flight(1, 9, "2025-01-01", "London", "LP")
        self.rm.create_flight(flight)

        # Test get flight by client ID, airline ID, and date
        retrieved_flight = self.rm.get_flight(
            1, 9, flight.get_date().isoformat())
        self.assertIsNotNone(
            retrieved_flight, "Flight should be retrieved successfully")
        self.assertEqual(retrieved_flight.get_date(), flight.get_date(
        ), "Retrieved flight date should match original")

        # Test get flight with existing client and airline IDs
        existing_flight = self.rm.get_flight(1, 9)
        self.assertIsNotNone(
            existing_flight, "Flight should be retrieved with existing client and airline IDs")

        # Test get flight with non-existing IDs
        non_existent_flight = self.rm.get_flight(199, 999)
        self.assertIsNone(
            non_existent_flight, "Flight retrieval should return None for non-existing IDs")

    def test_update_flight(self):
        """Test flight update functionality and handling of non-existent flights."""
        # Create test client, airline, and flight
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_client(client)
        self.rm.create_airline(airline)
        flight = Flight(1, 9, "2025-01-01", "London", "LP")
        self.rm.create_flight(flight)

        # Get the stored flight to extract the exact date format
        # Since we have special date handling for Flights records.
        stored_flights = [r for r in self.rm.records if r.get("Type") == "flight"
                          and r.get("Client_ID") == 1 and r.get("Airline_ID") == 9]
        if not stored_flights:
            self.fail("Flight was not created successfully")

        stored_date = stored_flights[0].get("Date")

        # Test successful flight update
        updated_flight = Flight(1, 9, stored_date, "London", "Liverpool")
        update_success = self.rm.update_flight(
            updated_flight, client_id=1, airline_id=9, date=stored_date)
        self.assertTrue(
            update_success, "Flight update should return True for existing flight")

        # Verify flight was updated correctly
        retrieved_flight = self.rm.get_flight(1, 9)
        self.assertEqual(retrieved_flight.get_end_city(),
                         "Liverpool", "End city should be updated to Liverpool")

        # Test update of non-existent flight
        non_existent_flight = Flight(
            199, 91, "2025-03-24T06:31:00", "NonExistentCity1", "NonExistentCity2")
        non_existent_update = self.rm.update_flight(
            flight=non_existent_flight,
            client_id=199,
            airline_id=91,
            date="2025-03-24T06:31:00"
        )
        self.assertFalse(non_existent_update,
                         "Update should return False for non-existent flight")

    def test_delete_flight(self):
        """Test flight deletion functionality and handling of non-existent flights."""
        # Create test client and airline
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        airline = Airline(9, "airline", "AirCX")
        self.rm.create_client(client)
        self.rm.create_airline(airline)

        # Create a test flight
        flight = Flight(1, 9, "2025-01-01", "London", "LP")
        self.rm.create_flight(flight)

        # Test successful flight deletion
        deletion_success = self.rm.delete_flight(
            1, 9, flight.get_date().isoformat())
        self.assertTrue(
            deletion_success, "Flight deletion should return True for existing flight")

        # Verify flight was deleted
        retrieved_flight = self.rm.get_flight(1, 9)
        self.assertIsNone(retrieved_flight,
                          "Flight should no longer exist after deletion")

        # Test deletion of non-existent flight
        non_existent_deletion = self.rm.delete_flight(199, 91)
        self.assertFalse(non_existent_deletion,
                         "Deletion should return False for non-existent flight")

    def test_search_flights(self):
        """Test flight search functionality with various search criteria."""
        # Create test client and airline
        client = Client(1, "client", "John", "123 St", "",
                        "", "London", "LONDON", "10001", "UK")
        airline = Airline(9, "airline", "AirCo")
        self.rm.create_client(client)
        self.rm.create_airline(airline)

        # Create test flights
        flight1 = Flight(1, 9, "2025-01-01", "London", "LP")
        flight2 = Flight(1, 9, "2025-01-01", "London", "Oxford")
        self.rm.create_flight(flight1)
        self.rm.create_flight(flight2)

        # Test search by start city
        results = self.rm.search_flights(start_city="London")
        self.assertEqual(
            len(results), 2, "Should find two flights departing from London")
        self.assertEqual(results[0].get_start_city(
        ), "London", "Retrieved flight should depart from London")

        # Test search by end city
        results = self.rm.search_flights(end_city="LP")
        self.assertEqual(
            len(results), 1, "Should find one flight arriving at LP")

        # Test search by date
        results = self.rm.search_flights(date=datetime(2025, 1, 1))
        self.assertEqual(
            len(results), 2, "Should find two flights on January 1, 2025")

        # Test search with non-existent date
        results = self.rm.search_flights(date=datetime(2025, 3, 20))
        self.assertEqual(
            len(results), 0, "Should find no flights on March 20, 2025")

        # Test search with non-existent city
        results = self.rm.search_flights(start_city="Cambridge")
        self.assertEqual(
            len(results), 0, "Should find no flights departing from Cambridge")


if __name__ == '__main__':
    unittest.main(verbosity=2)
