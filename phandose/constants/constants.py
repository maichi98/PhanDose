from pathlib import Path
import platform

__all__ = [
    "DIR_PHANTOM_LIBRARY",
    "DIR_PATIENT_HUB",
    "DIR_LOGS"
]

DIR_PHANTOM_LIBRARY_LINUX = "/home/maichi/.PhanDose/PhantomLib"
DIR_PHANTOM_LIBRARY_WINDOWS = fr"D:/PhanDose/PhantomLib"
DIR_PHANTOM_LIBRARY = DIR_PHANTOM_LIBRARY_LINUX if platform.system() == "Linux" else DIR_PHANTOM_LIBRARY_WINDOWS

DIR_PATIENT_HUB_LINUX = "/home/maichi/.PhanDose/PatientHub"
DIR_PATIENT_HUB_WINDOWS = fr"D:/PhanDose/PatientHub"
DIR_PATIENT_HUB = DIR_PATIENT_HUB_LINUX if platform.system() == "Linux" else DIR_PATIENT_HUB_WINDOWS

DIR_LOGS = str(Path(__file__).parent.parent.parent / "logs")
