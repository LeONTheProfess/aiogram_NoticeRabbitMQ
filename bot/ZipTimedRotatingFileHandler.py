import os
import zipfile

from logging.handlers import TimedRotatingFileHandler


class ZipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)

    def make_zip(self):
        dir_path, base_filename = os.path.split(self.baseFilename)
        logs_list = [f for f in os.listdir(dir_path)
                     if all([f.startswith(base_filename), f != base_filename, not f.endswith('.zip')])]
        if len(logs_list) >= self.backupCount:
            zipFilePath = os.path.join(dir_path, 'archive_{}.zip'.format(logs_list[0]))
            with zipfile.ZipFile(zipFilePath, 'w') as zip_file:
                for f in logs_list:
                    file = os.path.join(dir_path, f)
                    zip_file.write(file, f, compress_type=zipfile.ZIP_DEFLATED)
                    os.remove(file)

    def doRollover(self):
        if self.backupCount > 0:
            self.make_zip()
        super().doRollover()

    def getFilesToDelete(self):
        return []