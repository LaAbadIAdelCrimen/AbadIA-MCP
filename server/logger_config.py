import logging
import sys

def setup_logger():
    """
    Configures and returns a project-wide logger.
    """
    # Get the root logger
    logger = logging.getLogger("AbadIA")
    logger.setLevel(logging.INFO)

    # Create a handler to print to the console
    handler = logging.StreamHandler(sys.stdout)
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    # This prevents adding handlers multiple times if the function is called again
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# Create the global logger instance
log = setup_logger()
