import os


class PathParser:
    def __init__(self, path):

        self.jackFilesList = []
        self._parse_path(path)

    def _parse_path(self, path):

        if os.path.isfile(path):
            self._parse_file(path)
        elif os.path.isdir(path):
            self._parse_dir(path)
        else:
            print('%s is invalid path.' % path)

    def _parse_file(self, path):

        if path[-4:] != 'jack':
            return
        else:
            self.jackFilesList.append(path)

    def _parse_dir(self, path):

        filesList = os.listdir(path)

        for file in filesList:
            self._parse_path(path + '/' + file)

