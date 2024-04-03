from phandose.utils import (round_nearest,
                            cart_to_pol,
                            Get_Area)
from pathlib import Path
import pandas as pd
import numpy as np
import cv2


def _get_phantom_lib_dataframe(path_phantom_lib: Path) -> pd.DataFrame:
    """
    Create the Phantom Library DataFrame from the Phantom text files located at the given path.

    The DataFrame has three columns :
        - Phantom : Name of the Phantom text file
        - Position : Position of the Phantom (e.g. 'HFS', 'FFS')
        - Sex : Sex of the Phantom (e.g. 'M', 'F')

    :param path_phantom_lib: Path to the directory containing the phantom library text files.
    :return: pd.DataFrame, The Phantom Library DataFrame, with columns : ['Phantom', 'Position', 'Sex']
    """

    df_phantom_lib = pd.DataFrame({"Phantom": [filename.name for filename in path_phantom_lib.glob("*.txt")]})

    df_phantom_lib["Position"], df_phantom_lib["Sex"] = zip(*df_phantom_lib["Phantom"].map(lambda x: x.split("_")[1:3]))

    return df_phantom_lib


def _get_full_vertebrae_dataframe(df_contours: pd.DataFrame) -> pd.DataFrame:
    """
    Create a DataFrame indicating if each vertebra is fully within the contours.

    The function determines for each vertebra within the contours dataframe, whether it is fully
    within the contours or not, based on its z-coordinates.

    The DataFrame has two columns :
        - ROIName : Name of the vertebra
        - Full : Boolean indicating if the vertebra is fully within the contours

    :param df_contours: pd.DataFrame, The DataFrame containing the contours of the patient, each row
                        must contain the following columns : ['ROIName', 'z']

    :return:pd.DataFrame, the Full Vertebrae DataFrame, with columns : ['ROIName', 'Full']
    """

    list_vertebrae = df_contours.loc[df_contours['ROIName'].str.startswith('vertebrae'), 'ROIName'].unique().tolist()
    z_min, z_max = df_contours["z"].min(), df_contours["z"].max()

    # Compute the vertebrae_min_z and vertebrae_max_z for all vertebrae :
    vertebrae_z_min_max = df_contours.loc[df_contours['ROIName'].isin(list_vertebrae)] \
        .groupby('ROIName')['z'].agg(['min', 'max'])

    # Create a full vertebrae DataFrame :
    dict_full_vertebrae = [{"ROIName": vertebrae, "Full": (row["min"] > z_min) and (row["max"] < z_max)}
                           for vertebrae, row in vertebrae_z_min_max.iterrows()]

    df_full_vertebrae = pd.DataFrame(dict_full_vertebrae)

    return df_full_vertebrae


def _get_barycenter_dataframe(df_contours: pd.DataFrame) -> pd.DataFrame:
    """
    Create a DataFrame containing the barycenter of each contour from df_contours dataframe.

    The DataFrame has five columns :
        - Organ : Name of the organ of the contour
        - Rts :
        - Barx : x-coordinate of the barycenter
        - Bary : y-coordinate of the barycenter
        - Barz : z-coordinate of the barycenter

    :param df_contours: pd.DataFrame, The DataFrame containing the contours of the patient
    :return: pd.DataFrame, The Barycenter DataFrame, with columns : ['Organ', 'Rts', 'Barx', 'Bary', 'Barz']
    """

    # Compute the barycenter of each contour :
    df_barycenter = df_contours.groupby("ROIName")[["x", "y", "z"]].mean().reset_index()
    df_barycenter["Rts"] = 'Patient_Contours'

    df_barycenter = df_barycenter[["ROIName", "Rts", "x", "y", "z"]].rename(columns={"ROIName": "Organ",
                                                                                     "x": "Barx",
                                                                                     "y": "Bary",
                                                                                     "z": "Barz"})

    return df_barycenter


def _get_top_junction_dataframe(df_contours: pd.DataFrame,
                                df_barycenter: pd.DataFrame):

    """
    Create a DataFrame that indicates the top junction of the patient's contours.

    :param df_contours: pd.DataFrame,
    :param df_barycenter:
    :return:
    """

    list_organ_z = sorted(df_barycenter["Barz"].unique().tolist())
    list_delta_z = [t - s for s, t in zip(list_organ_z, list_organ_z[1:])]
    delta_z_mean = sum(list_delta_z) / len(list_delta_z)

    is_top_junction = True
    top_vertebra_z = df_barycenter["Barz"].max()

    if "skull" in df_contours["ROIName"].unique():

        skull_z_max = df_contours.loc[df_contours["ROIName"] == "skull", "z"].max()
        skull_z_min = df_contours.loc[df_contours["ROIName"] == "skull", "z"].min()

        top_vertebra_z = df_barycenter.loc[df_barycenter["Barz"] < (skull_z_min - 3 * delta_z_mean), "Barz"].max()
        is_top_junction = (skull_z_max == df_contours["z"].max())

    top_vertebra_x = df_barycenter.loc[df_barycenter["Barz"] == top_vertebra_z, "Barx"].values[0]
    top_vertebra_y = df_barycenter.loc[df_barycenter["Barz"] == top_vertebra_z, "Bary"].values[0]

    top_vertebra = df_barycenter.loc[df_barycenter["Barz"] == top_vertebra_z, 'Organ'].values[0]

    if is_top_junction:

        df_top_junction = df_contours.loc[df_contours["ROIName"] == 'body trunc'].copy()

        df_top_junction["Ecart"] = abs(df_top_junction["z"] - top_vertebra_z)

        ecart_min = df_top_junction["Ecart"].min()

        df_top_junction = df_top_junction.loc[df_top_junction["Ecart"] == ecart_min]

        df_contours = df_contours.loc[df_contours["z"] <= df_top_junction["z"].values[0]]

        df_area_top_junction = Get_Area(df_top_junction)

        df_area_top_junction["Centrality"] = abs(df_area_top_junction["Centrex"])

        center_min = df_area_top_junction["Centrality"].min()

        contour_num = df_area_top_junction.loc[df_area_top_junction["Centrality"] == center_min, "ROIContourNumber"].values[0]

        df_top_junction = df_top_junction.loc[df_top_junction["ROIContourNumber"] == contour_num]

        center = df_top_junction[["x", "y"]].to_numpy()

        center_int = np.array([center]).astype(np.int32)

        xul, yul, wrp, hrp = cv2.boundingRect(center_int)

        top_rectangle = np.array([[xul, yul], [xul, yul + hrp], [xul + wrp, yul + hrp], [xul + wrp, yul]])

        df_top_junction['Polar'] = df_top_junction.apply(lambda row: cart_to_pol((row['x'],
                                                                                  row['y'],
                                                                                  df_area_top_junction.iloc[0]['Centrex'],
                                                                                    df_area_top_junction.iloc[0]['Centrey'])), axis=1)

        df_top_junction['rpat'] = df_top_junction.apply(lambda row: row['Polar'][0], axis=1)
        df_top_junction['tpat'] = df_top_junction.apply(lambda row: row['Polar'][1], axis=1)

        df_top_junction = df_top_junction.drop_duplicates(subset=['tpat'], keep='last')
        return df_top_junction, top_rectangle


def filter_phantoms(dir_phantom_lib: Path | str,
                    df_contours: pd.DataFrame,
                    df_patient_characteristics: pd.DataFrame,
                    **kwargs):

    # Make sure path_phantom_lib is a Path object :
    dir_phantom_lib = Path(dir_phantom_lib)

    # Select only the contours of the patient that are not the body or the skin :
    df_contours = df_contours[~df_contours["ROIName"].isin(["body", "skin"])]
    df_contours[["Origine", "Section"]] = ["Patient", 0]

    # Create phantom_lib DataFrame :
    df_phantom_lib = _get_phantom_lib_dataframe(dir_phantom_lib)

    # Create full_vertebrae DataFrame :
    df_full_vertebrae = _get_full_vertebrae_dataframe(df_contours)

    list_full_vertebrae = df_full_vertebrae.loc[df_full_vertebrae["Full"], "ROIName"].tolist()
    full_vertebrae_z_max = df_contours.loc[df_contours["ROIName"].isin(list_full_vertebrae), "z"].max()
    full_vertebrae_z_min = df_contours.loc[df_contours["ROIName"].isin(list_full_vertebrae), "z"].min()

    full_vertebrae_size = full_vertebrae_z_max - full_vertebrae_z_min

    # Create barycenter DataFrame :
    df_barycenter = _get_barycenter_dataframe(df_contours)

    list_barycenter_z = sorted(df_barycenter["Barz"].unique().tolist())
    barycenter_delta_z = [t - s for s, t in zip(list_barycenter_z, list_barycenter_z[1:])]
    delta_z_mean = sum(barycenter_delta_z) / len(barycenter_delta_z)

