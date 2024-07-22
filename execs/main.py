from phandose.phantom_library import PhantomLibrary
from phandose.workspace import Workspace
from phandose import constants, utils

import time

# Set up logger :
logger = utils.get_logger(__name__)


def display_welcome_message():

    welcome_message = """
    ***************************************************************************
    *                                                                         *
    *                         WELCOME TO PHANDOSE                             *
    *                                                                         *
    ***************************************************************************
    
    PhanDose is designed to provide a user-friendly interface for
    the Phantom dosimetry software.
    
    ---------------------------------------------------------------------------
    NOTE : This software is still under development.
    ---------------------------------------------------------------------------
    
    If you encounter any issues, please report them to the developers.
    """
    print(welcome_message)


def display_menu():

    menu = """    
    
    Please select an option from the following menu (q to quit) :
    ---------------------------------------------------------------------------
    Workspace                                  Patient
    ---------                                  -------
        1. Display Workspace                       5. Run TotalSegmentator
        2. Add patient to Workspace                6. Filter phantoms  
        3. Remove patient from Workspace           7. Extend CT scan
        4. Select patient from Workspace           8. Run OOF
    ---------------------------------------------------------------------------
    """
    print(menu)


def handle_user_choice(user_input: str):

    match user_input:
        case '1':
            print("Displaying Workspace")
        case '2':
            print("Adding patient to Workspace")
        case '3':
            print("Removing patient from Workspace")
        case '4':
            print("Selecting patient from Workspace")
        case '5':
            print("Running TotalSegmentator")
        case '6':
            print("Filtering phantoms")
        case '7':
            print("Extending CT scan")
        case '8':
            print("Running OOF")
        case 'q':
            logger.debug("Exiting PhanDose Application")
            exit()
        case _:
            logger.error("Invalid choice. Please select a valid option from the menu.")
            return


def main():
    # Start the PhanDose Application :
    logger.debug("Starting PhanDose Application")

    display_welcome_message()

    # Load the Phantom Library :
    phantom_library = PhantomLibrary(constants.DIR_PHANTOM_LIBRARY)

    while True:
        # Display the menu :
        display_menu()

        # Get the user input :
        user_input = input("Enter your choice : ")

        # Handle the user choice :
        handle_user_choice(user_input)


if __name__ == '__main__':
    main()
