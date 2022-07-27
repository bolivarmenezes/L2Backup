import datetime
import devices.database.path_of_files as path_pass


class ManagerLog:

    def __init__(self, severity=3):
        self.severity = severity

    def log(self, string):
        outfile = open(path_pass.map_logs, "a+")
        timestamp = datetime.datetime.now().strftime("%Y %b %d-%H:%M:%S")
        outfile.write(timestamp + ": " + string + "\n")
        outfile.close()

        enable = True
        if enable:
            print(timestamp + ": " + string)
