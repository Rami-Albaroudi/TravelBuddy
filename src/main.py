"""
Main python script launching the Record Management System (RMS).

From the GUI folder, the TravelAgentApp class is imported.
The class will be used to lauch the RMS and create the principal GUI.
"""

# Importing the class responsible for the creation of the GUI.
from gui.gui import TravelAgentApp


def main():
    """
    Main function that launches the RMS and keeps it active.
    """
    app = TravelAgentApp()  # The GUI is created.
    app.mainloop()  # The GUI is kept running until the user close it.


# Conditional lanching the main function.
if __name__ == "__main__":
    main()
