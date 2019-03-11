import logging
import os
import time

"""
进程安全的日志日期切割类
"""


class SafeFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        """
         Use the specified filename for streamed logging
         """
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.suffix_time = ''

    def emit(self, record):
        """
        Emit a record.
        Always check time
        """
        try:
            if self.check_base_filename(record):
                self.build_base_filename()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

    def check_base_filename(self, record):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        time_tuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix, time_tuple) or not os.path.exists(
                self.baseFilename):
            # if self.suffix_time != time.strftime(self.suffix, time_tuple) or not os.path.exists(
            #        self.baseFilename + '.' + self.suffix_time):

            return 1
        else:
            return 0

    def build_base_filename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        current_time_tuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, current_time_tuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time
        self.mode = 'a'

        # create soft links
        index = self.baseFilename.rfind(".")
        os.unlink(self.baseFilename[:index])
        os.symlink(self.baseFilename, self.baseFilename[:index])

        if not self.delay:
            self.stream = self._open()
