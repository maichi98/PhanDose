from pathlib import Path
from typing import Union
import pandas as pd
import time
import os

# path_phantom_lib = Path(__file__).parent.parent / "PhantomLib"
PATH_PHANTOM_LIB = Path(fr"C:\Users\maichi\work\My Projects\PhanDose\PhantomLib")


def create_df_phantom_lib(path_phantom_lib: Union[Path, str]) -> pd.DataFrame:
    """
    function to create the phantom library dataframe :
    :param path_phantom_lib: Union[Path, str], path to the phantom library
    :return: pd.DataFrame, phantom library dataframe
    """
    L_phantom_lib = [filename for filename in os.listdir(path_phantom_lib) if filename.endswith(".txt")]
    df_phantom_lib = pd.DataFrame({"Phantom": L_phantom_lib})

    df_phantom_lib["Position"] = df_phantom_lib["Phantom"].map(lambda x: x.split("_")[1])
    df_phantom_lib["Sex"] = df_phantom_lib["Phantom"].map(lambda x: x.split("_")[2])

    return df_phantom_lib


def filter_phantoms(self):
    pass
