from phandose import utils

from pathlib import Path
import pandas as pd

# Set up logger :
logger = utils.get_logger("Phantom Library")


class PhantomLibrary:
    """
    Class to represent and manage a Phantom Library.

    In this version, the Phantom Library is a collection of phantom files (dataframe in .txt files)
    stored in a specified directory.

    Attributes
    ----------
    _dir_phantom_lib : (Path)
        a Path object that represents the directory of the Phantom Library

    Methods
    -------
    get_phantom(phantom_name: str) -> pd.DataFrame
        Retrieves a phantom from the Phantom Library as a DataFrame.

    add_phantom(df_phantom: pd.DataFrame, phantom_name: str)
        Adds a new phantom to the Phantom Library.

    get_phantom_dataframe() -> pd.DataFrame
        Generates a DataFrame from the Phantom text files located in the Phantom Library directory.

    display()
        Displays the Phantom Library DataFrame (using a rich table).
    """

    def __init__(self, dir_phantom_library: Path):
        """
        Initializes the Phantom Library with a specified directory

        Parameters
        ----------
        dir_phantom_library : (Path)
            The directory of the Phantom Library.
        """

        self._dir_phantom_lib = Path(dir_phantom_library)
        logger.debug(fr"Initialized Phantom Library with directory: {self._dir_phantom_lib}")

    def get_phantom(self, phantom_name: str) -> pd.DataFrame:
        """
        Retrieves a phantom from the phantom Library as a DataFrame.

        This method takes as input the name of a phantom and returns the phantom as a DataFrame
        if it exists in the Phantom Library. If the phantom does not exist, a FileNotFoundError is raised.

        Parameters
        ----------
        phantom_name : (str)
            The name of the phantom to retrieve.

        Returns
        -------
        pd.DataFrame
            A DataFrame representation of the phantom.

        Raises
        ------
        FileNotFoundError
            If the phantom does not exist in the Phantom Library.
        """

        logger.debug(fr"Attempting to retrieve phantom {phantom_name} from the Phantom Library")
        path_phantom = self._dir_phantom_lib / phantom_name

        if path_phantom.exists():
            logger.debug(fr"Phantom {phantom_name} found in the Phantom Library, loading phantom as DataFrame")
            return pd.read_csv(path_phantom, encoding="ISO-8859-1", sep="\t", header=0)
        else:
            logger.error(fr"Phantom {phantom_name} not found in the Phantom Library !")
            raise FileNotFoundError(f"Phantom {phantom_name} not found in the Phantom Library.")

    def add_phantom(self, df_phantom: pd.DataFrame, phantom_name: str):
        """
        Adds a new phantom to the Phantom Library.

        This method takes as input a phantom as a DataFrame and adds it to the Phantom Library.

         Parameters
        ----------
        df_phantom : (pd.DataFrame)
            The phantom DataFrame to add.

        phantom_name : (str)
            The phantom's name. This will be used as the filename for the phantom's text file in the Phantom Library.

        Raises
        ------
        FileExistsError
            If a phantom with the same name already exists in the Phantom Library.
        """

        logger.debug(fr"Attempting to add phantom {phantom_name} to the Phantom Library")
        path_phantom = self._dir_phantom_lib / phantom_name

        if path_phantom.exists():
            logger.error(f"Phantom {phantom_name} already exists in the Phantom Library !")
            raise FileExistsError(f"Phantom {phantom_name} already exists in the Phantom Library.")
        else:
            df_phantom.to_csv(path_phantom, sep="\t", index=False)
            logger.info(fr"Phantom {phantom_name} successfully added to the Phantom Library")

    def get_phantom_dataframe(self) -> pd.DataFrame:
        """
        This method generates a DataFrame from the Phantom text files located in the Phantom Library directory.

        The DataFrame has three columns:
            - Phantom: Name of the Phantom text file
            - Position: Position of the Phantom (e.g. 'HFS', 'FFS')
            - Sex: Sex of the Phantom (e.g. 'M', 'F')

        Returns
        -------
        pd.DataFrame
            The Phantom Library DataFrame, with columns: ['Phantom', 'Position', 'Sex']

        """

        logger.debug("Generating Phantom Library DataFrame")

        df_phantom_lib = pd.DataFrame({"Phantom": [filename.name for filename in self._dir_phantom_lib.glob("*.txt")]})
        df_phantom_lib["Position"], df_phantom_lib["Sex"] = zip(
            *df_phantom_lib["Phantom"].map(lambda x: x.split("_")[1:3]))

        logger.debug("Phantom Library DataFrame generated successfully")
        return df_phantom_lib

    def display(self):
        """
        Displays the Phantom Library DataFrame.

        This method generates the Phantom Library DataFrame and displays it in a formatted table
        using the rich library.
        """

        logger.debug(fr"Displaying Phantom Library DataFrame")

        from rich.console import Console
        from rich.table import Table

        df_phantom_lib = self.get_phantom_dataframe()

        console = Console()
        table = Table(show_header=True, header_style="bold magenta")

        for column in df_phantom_lib.columns:
            table.add_column(column)

        for _, row in df_phantom_lib.iterrows():
            table.add_row(*map(str, row))

        console.print(table)
        logger.debug("Phantom Library DataFrame displayed successfully")
