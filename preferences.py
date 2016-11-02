import os


class Preferences:
    # Load the default path for the preferences file
    file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname("preferences.py"), 'data')), 'prefs.txt')
    # Make an empty dictionary for the preferences
    list = {}

    def parse_raw(self, lines):
        """
        Stores the lines as key-value pairs in the dictionary

        :param lines: A list of strings
        """
        # For each line in the file
        for line in lines:
            # split the line up in to a key (value[0]) and a value (value[1])
            values = line.split("=")
            if values[0] or values[1]:
                # Then add them to the dictionary
                self.list[values[0]] = values[1]

    def __init__(self, file_path):
        self.file_path = file_path
        self.__init__()

    def __init__(self):
        # Only parse the file if it exists
        if os.path.exists(self.file_path):
            # Create an empty list for storing the lines
            lines = []

            # Open the file in readmode
            file = open(self.file_path, 'r')
            # Loop through all the lines in the file and put the strings in the lines-list
            for line in file:
                lines.append(line)

            # Then convert the lines into the dictionary
            self.parse_raw(lines)
            # Close the file
            file.close()
        else:
            print("File does not exist")

    def get_preference(self, key):
        """
        Gets the preference for the given key

        :param key: The key of the preference
        :return: The value that comes with the key
        """
        return self.list.get(key, -1)

    def set_preference(self, key, value):
        """
        Sets the preference value for the given key

        :param key: A <String> representing the key
        :param value: The value to be stored at the given key
        """
        # Store the change in the dictionary
        self.list[key] = value

        # Store the change on the hard disk
        file = open(self.file_path, 'w')
        for key in self.list:
            file.write(key + "=" + self.list[key] + "\n")
        file.close()
