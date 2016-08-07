import logging
import datetime
import json

class JSONFormatter(logging.Formatter):

    def format(self, record):
        """Formats log record into JSON Format
        """
        message = super().format(record)
        log_message = dict(
            name=record.name,
            timestamp=str(datetime.datetime.now()),
            level=record.levelname,
            message=record.msg,
            exc_info=record.exc_info,
            path_name=record.pathname,
            lineno=record.lineno,
            module=record.module,
            file_name=record.filename,
            func_name=record.funcName
        )
        return json.dumps(log_message)
