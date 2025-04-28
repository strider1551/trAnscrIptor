import logging
import logging.handlers
import sys

from pathlib import Path

class CustomLogFormatter(logging.Formatter):
    """
    A custom formatter for log messages that adds color to terminal output
    but not to file output.
    """
    # Define your desired format string
    FORMAT = "[%(asctime)s] %(levelname)-8s - %(filename)s:%(lineno)-5d - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Define ANSI escape codes for colors
    COLOR_CODES = {
        logging.DEBUG: "\x1b[36;20m",  # Cyan
        logging.INFO: "",   
        logging.WARNING: "\x1b[33;20m", # Yellow
        logging.ERROR: "\x1b[31;20m",   # Red
        logging.CRITICAL: "\x1b[41;37m" # White on Red background
    }
    RESET_CODE = "\x1b[0m" # Reset to default color

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt or self.FORMAT, datefmt=datefmt or self.DATE_FORMAT, style=style)
        # Store the output stream when the formatter is associated with a handler
        self.stream = None

    def format(self, record):
        """
        Formats the log record, adding color if the output stream is a TTY.
        """
        # Get the default formatted message
        log_message = super().format(record)

        # Check if the output stream is a TTY (terminal) and if so add color
        is_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if is_tty:
            # Add color codes based on the log level
            level_color = self.COLOR_CODES.get(record.levelno)
            if level_color:
                # Apply color to the entire formatted line
                log_message = f"{level_color}{log_message}{self.RESET_CODE}"

        return log_message

def setup_logging(level=logging.DEBUG, log_file=None, max_bytes=1024*1024*5, backup_count=5):
    """
    Configures the root logger with a StreamHandler and optionally a RotatingFileHandler.

    Args:
        level: The minimum logging level to capture (e.g., logging.DEBUG).
        log_file: Path to the log file for file logging. If None, no file handler is added.
        max_bytes: The maximum size of the log file before rotation (in bytes).
                   Used by RotatingFileHandler. Defaults to 5MB.
        backup_count: The number of backup log files to keep. Used by RotatingFileHandler.
                      Defaults to 5.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Prevent adding duplicate handlers if the function is called multiple times
    # Clear existing handlers first for a clean setup, especially useful in testing
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)


    # Create and add StreamHandler for console output
    console_handler = logging.StreamHandler(sys.stdout)
    # Use a new instance of the custom formatter for each handler
    console_formatter = CustomLogFormatter()
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Create and add RotatingFileHandler for file output if a log_file is specified
    if log_file:
        try:
            if Path(log_file).exists():
                rollover_needed = True
            else:
                rollover_needed = False
            # Use RotatingFileHandler for automatic rotation based on size
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            # Use a new instance of the custom formatter for the file handler
            # The isatty() check inside the formatter will correctly detect
            # that the file stream is not a TTY and will not add color codes.
            file_formatter = CustomLogFormatter()
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
            if rollover_needed:
                file_handler.doRollover()
            logging.debug(f"Logging to file configured: {log_file}")
        except Exception as e:
            # Log an error to the console if file logging setup fails
            logging.error(f"Failed to set up file logging to {log_file}: {e}")


    logging.debug("Logging system configured.")

# Testing 
# if __name__ == "__main__":
#     setup_logging(level=logging.DEBUG, log_file="test_application.log", max_bytes=1024*10, backup_count=3)
#     logger = logging.getLogger(__name__)
#     logger.debug("This is a debug message.")
#     logger.info("This is an info message.")
#     logger.warning("This is a warning message.")
#     logger.error("This is an error message.")
#     logger.critical("This is a critical message.")
#     # Generate enough logs to trigger rotation if max_bytes is small
#     # for i in range(2000):
#     #     logger.info(f"Log entry {i}")


