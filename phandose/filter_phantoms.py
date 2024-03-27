from pathlib import Path
import pandas as pd
import os


def filter_phantoms(df_phantom_lib: pd.DataFrame,
                    df_patient_characteristics: pd.DataFrame,
                    df_contours: pd.DataFrame,
                    **kwargs):

    list_vertebrae = [
        "vertebrae C1", "vertebrae C2", "vertebrae C3", "vertebrae C4", "vertebrae C5", "vertebrae C6", "vertebrae C7",
        "vertebrae T1", "vertebrae T2", "vertebrae T3", "vertebrae T4", "vertebrae T5", "vertebrae T6", "vertebrae T7",
        "vertebrae T8", "vertebrae T9", "vertebrae T10", "vertebrae T11", "vertebrae T12",
        "vertebrae L1", "vertebrae L2", "vertebrae L3", "vertebrae L4", "vertebrae L5",
        "vertebrae S1"
    ]

    df_contours = df_contours.loc[~df_contours["ROIName"].isin(["body", "skin"])].copy()
    df_contours[["Origine", "Section"]] = ["Patient", "0"]
    patient_bottom_z = df_contours["z"].min()
    patient_top_z = df_contours["z"].max()
    list_patient_contours = df_contours["ROIName"].unique().tolist()




