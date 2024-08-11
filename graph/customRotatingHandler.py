import logging
from logging.handlers import RotatingFileHandler
import os

class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None, delay=False):
        self.baseFilename = filename
        super(CustomRotatingFileHandler, self).__init__(filename, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)
        
    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:
            # Rotate the existing log files
            for i in range(self.backupCount - 1, 0, -1):
                sfn = f"{self.baseFilename[:-6]}{i}.cypher"
                dfn = f"{self.baseFilename[:-6]}{i + 1}.cypher"
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = f"{self.baseFilename[:-6]}1.cypher"
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)

        if not self.delay:
            self.stream = self._open()



class MyLogger():
    def __init__(self, log_file, log_file_size, no_of_logs) -> None:
        self.log_filename = log_file
        self.log_filesize = log_file_size
        self.no_of_logs = no_of_logs

        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.DEBUG)

        # Create a handler that writes log messages to a file,
        handler = CustomRotatingFileHandler(self.log_filename, maxBytes=self.log_filesize, backupCount=self.no_of_logs)
        handler.setLevel(logging.DEBUG)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)



    @classmethod
    def get_logger(cls, LOG_FILENAME, EACH_LOG_FILE_SIZE, NUM_OF_LOGS):
        # Set up a logger


        return cls(LOG_FILENAME, EACH_LOG_FILE_SIZE, NUM_OF_LOGS).logger
