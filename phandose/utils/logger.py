from phandose import constants

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
            'name_width': 15,
            "level_width": 8
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default'
        },
        'rootFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{constants.DIR_LOGS}/phandose_app.log',
            'mode': 'a',  # Append mode
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,  # Keep 3 backup files
            'level': 'DEBUG',
            'formatter': 'file_formatter'
        },
        'modalityFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{constants.DIR_LOGS}/modalities.log',
            'mode': 'a',  # Append mode
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,  # Keep 3 backup files
            'level': 'DEBUG',
            'formatter': 'file_formatter'
        },
        'patientFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{constants.DIR_LOGS}/patients.log',
            'mode': 'a',  # Append mode
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,  # Keep 3 backup files
            'level': 'DEBUG',
            'formatter': 'file_formatter'
        },
        'patientHubFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{constants.DIR_LOGS}/patient_hub.log',
            'mode': 'a',  # Append mode
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,  # Keep 3 backup files
            'level': 'DEBUG',
            'formatter': 'file_formatter'
        },
        'phantomLibraryFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{constants.DIR_LOGS}/phantom_library.log',
            'mode': 'a',  # Append mode
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,  # Keep 3 backup files
            'level': 'DEBUG',
            'formatter': 'file_formatter'
        }
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'rootFileHandler']
        },
        'modalities': {
            'level': 'DEBUG',
            'handlers': ['modalityFileHandler']
        },
        'patients': {
            'level': 'DEBUG',
            'handlers': ['patientFileHandler']
        },
        'PatientHub': {
            'level': 'DEBUG',
            'handlers': ['patientHubFileHandler']
        },
        'PhantomLibrary': {
            'level': 'DEBUG',
            'handlers': ['phantomLibraryFileHandler']
        }
    }
}
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
