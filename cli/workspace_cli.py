from phandose import constants, utils


# Set up logger :
logger = utils.get_logger(__name__)


def workspace_cli(workspace_input: str):
    """
    This function is used to handle the workspace menu options.
    """
    # Handle the user choice :
    match workspace_input:
        case '1':
            logger.debug("Adding patient to Workspace")
        case '2':
            logger.debug("Removing patient from Workspace")
        case '3':
            logger.debug("Selecting patient from Workspace")
        case 'q':
            logger.debug("Exiting Workspace Menu")
            return
        case _:
            logger.error("Invalid choice. Please select a valid option from the menu.")
            return
