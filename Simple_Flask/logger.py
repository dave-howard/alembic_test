import os
import datetime


class Logger:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.log_dir = "logs"
        self.log_file = "simple_flask.log"
        if not os.path.exists(os.path.join(self.base_dir, self.log_dir)):
            os.mkdir(os.path.join(self.base_dir, self.log_dir))

    def log(self, text):
        file  = os.path.join(self.base_dir, self.log_dir, self.log_file)
        dt = datetime.datetime.now()
        text = Logger.clean_string(text)
        with open(file, "a") as f:
            f.write("{0:02}-{1:02}-{2:02} {3:02}:{4:02}:{5:02} {6}".format(
                dt.year, dt.month, dt.day, dt.hour, dt.min, dt.second, text))

    @staticmethod
    def clean_string(string):
        string = str(string)
        if '\n' not in string:
            string = string + "\n"
        string = string.replace("&", "&amp;")
        return string
