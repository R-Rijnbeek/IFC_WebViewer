import logging
from functools import wraps

class LogStream():
    def __init__(self, MAX_RECORDS ):

        self.logs = []
        self.max_records = MAX_RECORDS
        self.lines = 0

    def write(self, str):
        print(str[:-1])
        if (self.lines >= self.max_records ):
            self.logs.append(str)
            self.logs.pop(0)
        else:
            self.logs.append(str)
            self.lines +=1

    def flush(self):
        pass

    def __str__(self):
        return "".join(self.logs)

    def _getStream(self):
        return "".join(self.logs)

class ApplicationLogger():
    def __init__(self,logname):
        self.logname = logname
        self._LOGGER = None
        self._activated = False
        self.debugs = 0
        self.infos = 0
        self.warnings = 0
        self.errors = 0
        self.criticals = 0
        self._logginglevels =  {
            'CRITICAL' : logging.CRITICAL,
            'ERROR' : logging.ERROR,
            'WARNING' : logging.WARNING,
            'INFO' : logging.INFO,
            'DEBUG' : logging.DEBUG
        }

    def init_app(self,APP):
        if APP.config["LOGGING_SERVICE"]:
            self.stream = LogStream(APP.config["MAX_LOG_RECORDS"])
            logging.basicConfig(
                stream=self.stream, 
                level=self._logginglevels[APP.config["LOGGING_LEVELS"]], 
                format=APP.config["LOGGER_FORMAT"]
            )
            self._LOGGER = logging.getLogger(self.logname)
            self._activated = True
            return True
        else:
            print("Logging service is not activated")
            return True

    def _isActive(f):
        @wraps(f)
        def inner1(inst,*args, **kwargs):
            if inst._activated:
                return f(inst,*args, **kwargs)
            else:
                #print("Logger is not activated so the method is not processed")
                return
        return inner1

    @_isActive
    def getStream(self):
        return self.stream._getStream()

    @_isActive
    def debug(self, str):
        self.debugs +=1
        self._LOGGER.debug(str)
    
    @_isActive
    def info(self, str):
        self.infos +=1
        self._LOGGER.info(str)

    @_isActive
    def warning(self, str):
        self.warnings +=1
        self._LOGGER.warning(str)

    @_isActive
    def error(self, str):
        self.errors += 1
        self._LOGGER.error(str)

    @_isActive
    def critical(self, str):
        self.criticals += 1
        self._LOGGER.critical(str)


# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass
