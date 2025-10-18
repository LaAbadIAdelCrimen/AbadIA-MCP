import logging
import sys
from server.ansi_colors import RESET, BRIGHT_YELLOW, BRIGHT_RED, GREEN

class ColoredFormatter(logging.Formatter):
    """
    A custom log formatter that adds ANSI color codes to log level names.
    """
    
    LOG_LEVEL_COLORS = {
        logging.DEBUG: GREEN,
        logging.INFO: GREEN,
        logging.WARNING: BRIGHT_YELLOW,
        logging.ERROR: BRIGHT_RED,
        logging.CRITICAL: BRIGHT_RED,
    }

    def format(self, record):
        color = self.LOG_LEVEL_COLORS.get(record.levelno)
        record.levelname = f"{color}{record.levelname}{RESET}"
        return super().format(record)

def setup_logger():
    """
    Configures and returns a project-wide logger with colored output.
    """
    logger = logging.getLogger("AbadIA")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Create the global logger instance
log = setup_logger()
