import os


class Preferences:
    file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname("preferences.py"), 'data')), 'prefs.txt')
    list = {}

    def parse_raw(self, lines):
        for line in lines:
            values = line.split("=")
            if values[0] or values[1]:
                self.list[values[0]] = values[1]

    def __init__(self, file_path):
        self.file_path = file_path
        self.__init__()

    def __init__(self):
        if os.path.exists(self.file_path):
            lines = []

            file = open(self.file_path, 'r')
            for line in file:
                lines.append(line)
            self.parse_raw(lines)
            file.close()
        else:
            print("File does not exist")

    def getPreference(self, name):
        return self.list.get(name, -1)

    def setPreference(self, name, value):
        self.list[name] = value
        file = open(self.file_path, 'w')
        for key in self.list:
            file.write(key + "=" + self.list[key] + "\n")
        file.close()
