from phandose.phantom_library import PhantomLibrary
from phandose.workspace import Workspace
from phandose import constants, utils

import time

# Set up logger :
logger = utils.get_logger(__name__)


def display_welcome_message():

    welcome_message = """
    ***********************************************************************************************************
    *                                                                                                         *
    *                                          WELCOME TO PHANDOSE                                            *
    *                                                                                                         *
    ***********************************************************************************************************
    PhanDose is designed to provide a user-friendly interface for
    the Phantom dosimetry software.
    
    -----------------------------------------------------------------------------------------------------------
    NOTE : This software is still under development.
    -----------------------------------------------------------------------------------------------------------
    
    If you encounter any issues, please report them to the developers.
    """
    print(welcome_message)


def display_menu():

    menu = """    
    
    Please select an option from the following menu (q to quit) :
    -----------------------------------------------------------------------------------------------------------
    Workspace                               Patient                        Phantom 
    ---------                               -------                        -------
        1. Display Workspace                    5. Run TotalSegmentator        9. Display Phantom Library
        2. Add patient to Workspace             6. Filter phantoms            10. Add phantom to Library  
        3. Remove patient from Workspace        7. Extend CT scan             11. Remove phantom from Library
        4. Select patient from Workspace        8. Run OOF                    12. Get phantom from Library
    -----------------------------------------------------------------------------------------------------------
    """
    print(menu)


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
        match user_input:

            case '1':
                logger.debug("Displaying Workspace")
            case '2':
                logger.debug("Adding patient to Workspace")
            case '3':
                logger.debug("Removing patient from Workspace")
            case '4':
                logger.debug("Selecting patient from Workspace")
            case '5':
                logger.debug("Running TotalSegmentator")
            case '6':
                logger.debug("Filtering phantoms")
            case '7':
                logger.debug("Extending CT scan")
            case '8':
                logger.debug("Running OOF")
            case '9':
                print("Displaying the Phantom Library : ")
                phantom_library.display()
                print("\n")

            case '10':
                logger.debug("Adding phantom to Library")
            case '11':
                logger.debug("Removing phantom from Library")
            case '12':
                logger.debug("Getting phantom from Library")

            case 'q':
                logger.debug("Exiting PhanDose Application")
                exit()
            case _:
                logger.error("Invalid choice. Please select a valid option from the menu.")
                return


if __name__ == '__main__':
    main()
