from phandose.utils import (round_nearest,
                            cart_to_pol,
                            Get_Area)
from pathlib import Path
import pandas as pd


def filter_phantoms(path_phantom_lib: Path | str,
                    df_patient_characteristics: pd.DataFrame,
                    df_contours: pd.DataFrame,
                    **kwargs):

    path_phantom_lib = Path(path_phantom_lib)

    # Create phantom_lib :
    df_phantom_lib = pd.DataFrame({"Phantom": [filename.name for filename in path_phantom_lib.glob("*.txt")]})
    df_phantom_lib["Position"], df_phantom_lib["Sex"] = zip(*df_phantom_lib["Phantom"].map(lambda x: x.split("_")[1:3]))

    # List of vertebrae :
    list_selected_vertebrae = [
        "vertebrae C1", "vertebrae C2", "vertebrae C3", "vertebrae C4", "vertebrae C5", "vertebrae C6", "vertebrae C7",
        "vertebrae T1", "vertebrae T2", "vertebrae T3", "vertebrae T4", "vertebrae T5", "vertebrae T6", "vertebrae T7",
        "vertebrae T8", "vertebrae T9", "vertebrae T10", "vertebrae T11", "vertebrae T12",
        "vertebrae L1", "vertebrae L2", "vertebrae L3", "vertebrae L4", "vertebrae L5",
        "vertebrae S1"
    ]

    df_contours = df_contours[~df_contours["ROIName"].isin(["body", "skin"])]
    df_contours[["Origine", "Section"]] = ["Patient", 0]

    list_contours = df_contours["ROIName"].unique().tolist()

    bottom_z, top_z = df_contours["z"].min(), df_contours["z"].max()

    list_vertebrae = [roi_name for roi_name in list_contours if roi_name.split(' ')[0] == "vertebrae"]

    for vertebrae in list_vertebrae:

        vertebrae_bottom_z = df_contours[df_contours["ROIName"] == vertebrae]["z"].min()
        vertebrae_top_z = df_contours[df_contours["ROIName"] == vertebrae]["z"].max()

        df0 = pd.DataFrame(data={"ROIName": [vertebrae],
                                 "Full": [(vertebrae_bottom_z > bottom_z) and (vertebrae_top_z > top_z)]})
        df_full_vertebrae = pd.concat([df_full_vertebrae, df0], ignore_index=True)

    return df_full_vertebrae

