from phandose import constants

from datetime import datetime, timezone
from pathlib import Path
from tqdm import tqdm
import logging.config
import logging


class CenterAlignedFormatter(logging.Formatter):
    """
    A custom formatter for center aligning the logger name and log level.

    Parameters
    ----------
    fmt : (str | None)
        The log message format.

    datefmt : (str | None)
        The date format.

    style : (Literal["%", "{", "$"])
        The format style.

    name_width : (int)
        The width of the logger name.

    level_width : (int)
        The width of the log level.

    Methods
    -------
    format(record)
        Format the log record.

    """

    def __init__(self, fmt=None, datefmt=None, style='%', name_width=15, level_width=8):

        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.name_width = name_width
        self.level_width = level_width

    def format(self, record):
        """
        Format the log record.

        Parameters
        ----------
        record : (logging.LogRecord)
            The log record.

        Returns
        -------
        str
            The formatted log record.

        """

        def center(text, width):
            length = len(text)
            total_padding = width - length
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            return f"{' ' * left_padding}{text}{' ' * right_padding}"

        # Center align the logger name :
        record.name = center(record.name, self.name_width)

        # Center align the log level :
        record.levelname = center(record.levelname, self.level_width)

        return super().format(record)


class TqdmLoggingHandler(logging.StreamHandler):
    """
    A custom logging handler for displaying log messages in a tqdm progress bar.

    Methods
    -------
    emit(record)
        Emit the log record.

    """

    def emit(self, record):
        """
        Emit the log record.

        Parameters
        ----------
        record : (logging.LogRecord)
            The log record.

        """

        try:
            msg = self.format(record)
            tqdm.write(msg)

        except Exception:
            self.handleError(record)


DICT_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(message)s'
        },
        'file_formatter': {
            '()': CenterAlignedFormatter,
            'format': f'%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'name_width': 40,
            "level_width": 8
        }
    },
    'handlers': {
        'rootFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{constants.DIR_LOGS}/phandose.log',
            'mode': 'a',  # Append mode
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,  # Keep 3 backup files
            'level': 'DEBUG',
            'formatter': 'file_formatter'
        },
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['rootFileHandler']
        },

    }
}

logging.getLogger("numexpr.utils").disabled = True
logging.config.dictConfig(DICT_LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger object for logging messages.

    Parameters
    ----------
    name : (str)
        The name of the logger.

    Returns
    -------
    logging.Logger
        A logger object.

    """

    return logging.getLogger(name)


def add_file_handler_to_root(dir_log: Path = constants.DIR_LOGS,
                             prefix: str = "phandose",
                             level: int = logging.DEBUG,
                             timezone_info=timezone.utc):
    """
    Add a per-run file handler to the root logger.

    Parameters
    ----------
    dir_log : (Path)
        Directory where log files will be stored. Defaults to constants.DIR_LOGS.

    prefix : (str)
        Prefix for the log file name. Defaults to "phandose".

    level : (int)
        Logging level for the file handler. Defaults to logging.DEBUG.

    timezone_info : (timezone)
        Timezone for the timestamp in the log file name. Defaults to UTC.

    """

    try:
        # Create the log directory if it does not exist
        dir_log.mkdir(parents=True, exist_ok=True)

        # Update the log file name
        timestamp = datetime.now(timezone_info).strftime("%Y%m%d_%H%M%S")
        path_log_file = dir_log / f"{prefix}_{timestamp}.log"

        # Check if a similar file handler already exists
        root_logger = logging.getLogger('root')

        # Create the file handler
        file_handler = logging.FileHandler(path_log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(CenterAlignedFormatter(
            fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            name_width=40,
            level_width=8
        ))

        # Add the file handler to the root logger
        root_logger.addHandler(file_handler)

        logging.getLogger('phandose.utils.logger').info(f"Per-run logging enabled: {str(path_log_file)}")
    except Exception as e:
        logging.getLogger('phandose.utils.logger').error(f"Failed to add file handler: {e}")


def enable_tqdm_logging(log_level: int = logging.INFO):
    """
    Add a TqdmLoggingHandler to the root logger

    Parameters
    ----------
    log_level : int
        Logging level for the tqdm handler. Defaults to logging.INFO

    """

    # Get the root logger :
    root_logger = logging.getLogger('root')

    # Add the TqdmLoggingHandler :
    tqdm_handler = TqdmLoggingHandler()
    tqdm_handler.setLevel(log_level)
    tqdm_handler.setFormatter(logging.Formatter('%(message)s'))
    root_logger.addHandler(tqdm_handler)

    # Log the change :
    get_logger('phandose.utils.logger').debug("TQDM-compatible logging enabled.")


def enable_console_logging(log_level: int = logging.INFO):
    """
    Add a console logging handler to the root logger.

    Parameters
    ----------
    log_level : int
        Logging level for the console handler. Defaults to logging.INFO

    """

    # Get the root logger :
    root_logger = logging.getLogger('root')

    # Add the console handler :
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    root_logger.addHandler(console_handler)

    # Log the change :
    logging.getLogger('phandose.utils.logger').debug("Console logging enabled.")
