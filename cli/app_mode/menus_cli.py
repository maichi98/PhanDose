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


def main_menu():

    menu = """    
    Please select an option from the following menu (q to quit):
    -----------------------------------------------------------------------------------------------------------
    1. Access Patient Hub                  - Manage Patients
    2. create Temporary Workspace          - Create a temporary workspace 
    3. Access Phantom Library              - Access the phantom library
    -----------------------------------------------------------------------------------------------------------
    """

    print(menu)


def workspace_menu():

    menu = """    
    Please select an option from the following menu (q to quit):
    -----------------------------------------------------------------------------------------------------------
    Workspace Management
    --------------------
    1. Add patient to Workspace
    2. Remove patient from Workspace
    3. Select patient from Workspace
    -----------------------------------------------------------------------------------------------------------
    """

    print(menu)


def phantom_menu():

    menu = """    
    Please select an option from the following menu (q to quit):
    -----------------------------------------------------------------------------------------------------------
    Phantom Library
    ---------------
    1. Add phantom to Library
    2. Remove phantom from Library
    3. Get phantom from Library
    -----------------------------------------------------------------------------------------------------------
    """

    print(menu)
