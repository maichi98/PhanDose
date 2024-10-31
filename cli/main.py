from cli.menus_cli import display_welcome_message, main_menu, workspace_menu
from cli.phantom_library_cli import phantom_library_cli
from cli.workspace_cli import workspace_cli

from phandose.phantom_library import PhantomLibrary
from phandose import constants, utils

import time

# Set up logger :
logger = utils.get_logger(__name__)


def main():
    # Start the PhanDose Application :
    logger.debug("Starting PhanDose Application")
    display_welcome_message()

    # Load the Phantom Library :
    phantom_library = PhantomLibrary(constants.DIR_PHANTOM_LIBRARY)

    while True:
        # Display the menu :
        main_menu()

        # Get the user input :
        user_input = input("Enter your choice : ")

        # Handle the user choice :
        match user_input:

            case '1':
                while True:
                    workspace_menu()
                    workspace_input = input("Enter your choice : ")

                    if workspace_input == "b":
                        break

                    workspace_cli(workspace_input)

            case '2':
                pass
            case '3':
                phantom_library_cli()

            case 'q':
                logger.debug("Exiting PhanDose Application")
                exit()
            case _:
                logger.error("Invalid choice. Please select a valid option from the menu.")
                return


if __name__ == '__main__':
    main()
