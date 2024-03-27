from pathlib import Path
import pandas as pd


def create_df_phantom_lib(path_phantom_lib: Path | str) -> pd.DataFrame:
    """
    function to create the phantom library dataframe :
    :param path_phantom_lib: Union[Path, str], path to the phantom library
    :return: pd.DataFrame, phantom library dataframe
    """

    path_phantom_lib = Path(path_phantom_lib)

    list_phantom_lib = [filename.name for filename in path_phantom_lib.glob("*.txt")]
    df_phantom_lib = pd.DataFrame({"Phantom": list_phantom_lib})

    df_phantom_lib["Position"] = df_phantom_lib["Phantom"].map(lambda x: x.split("_")[1])
    df_phantom_lib["Sex"] = df_phantom_lib["Phantom"].map(lambda x: x.split("_")[2])

    return df_phantom_lib
