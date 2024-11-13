from cli.app_mode.menus_cli import display_welcome_message, main_menu, workspace_menu
from cli.app_mode.phantom_library_cli import phantom_library_cli
from cli.app_mode.workspace_cli import workspace_cli

from phandose.workspace import Workspace
from phandose.patient_hub import PatientHub
from phandose import utils
from pathlib import Path

# Set up logger :
logger = utils.get_logger(__name__)


def main():
    # Start the PhanDose Application :
    logger.debug("Starting PhanDose Application")
    display_welcome_message()

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
                dir_temp_patient_hub = Path("/media/maichi/T7/temp PatientHub")

                patient_hub = PatientHub(dir_temp_patient_hub)
                workspace = Workspace(patient_hub)

                dir_src_patient = Path("/sample_data/AGORL_P1")

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
