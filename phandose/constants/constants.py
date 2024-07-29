from pathlib import Path
import platform

__all__ = [
    "DIR_PHANTOM_LIBRARY",
    "DIR_WORKSPACE",
    "DIR_LOGS"
]

DIR_PHANTOM_LIBRARY_LINUX = "/home/maichi/.PhanDose/PhantomLib"
DIR_PHANTOM_LIBRARY_WINDOWS = fr"D:/PhanDose/PhantomLib"
DIR_PHANTOM_LIBRARY = DIR_PHANTOM_LIBRARY_LINUX if platform.system() == "Linux" else DIR_PHANTOM_LIBRARY_WINDOWS

DIR_WORKSPACE_LINUX = "/home/maichi/.PhanDose/Workspace"
DIR_WORKSPACE_WINDOWS = fr"D:/PhanDose/Workspace"
DIR_WORKSPACE = DIR_WORKSPACE_LINUX if platform.system() == "Linux" else DIR_WORKSPACE_WINDOWS

DIR_LOGS = str(Path(__file__).parent.parent.parent / "logs")
