from pathlib import Path

__all__ = [
    "DIR_PHANTOM_LIBRARY",
    "DIR_WORKSPACE",
    "DIR_LOGS"
]

DIR_PHANTOM_LIBRARY = "/home/maichi/.PhanDose/PhantomLib"
DIR_WORKSPACE = "/home/maichi/.PhanDose/Workspace"

DIR_LOGS = str(Path(__file__).parent.parent.parent / "logs")
