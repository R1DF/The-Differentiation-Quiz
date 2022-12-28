# Imports
import toml

# Configurations class
class Configurations:
    def __init__(self, path):
        # Getting path and full configurations dictionary
        self.path = path
        self.data = toml.load(path)

        # Getting inner values for ease
        self.program_data = self.data["program"]
        self.defaults = self.data["defaults"]

