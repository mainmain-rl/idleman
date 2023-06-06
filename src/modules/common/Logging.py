
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    getLogger,
    INFO,
    Logger,
    WARNING,
    basicConfig
)

class ErrorManager:
    def __init__(self,log_level="INFO",name=__name__):
        log_level_mapping = {
            "DEBUG": DEBUG,
            "INFO": INFO,
            "WARNING": WARNING,
            "ERROR": ERROR,
            "CRITICAL": CRITICAL
        }
        logger = getLogger(name)
        logger.setLevel(log_level_mapping[log_level])
        log_format = "{\"time\":\"%(asctime)s\",\"level\":\"%(levelname)s\",\"name\":\"%(name)s\",\"message\":\"%(message)s\"}"
        basicConfig(format=log_format)
        self.logger = logger
    
    def log_info(self, info_message):
        """Log an error message."""
        self.logger.info(info_message)
        
    def log_error(self, error_message):
        """Log an error message."""
        self.logger.error(error_message)
    
    def handle_exception(self, error_message, exception):
        """Handle an exception by logging an error message and the exception details."""
        self.logger.error(error_message, exc_info=True)
    
    def handle_critical(self, error_message,exception):
        """Handle a critical error by logging an error message and raising a SystemExit exception."""
        self.logger.critical(error_message, exc_info=True)
        raise SystemExit(1)

