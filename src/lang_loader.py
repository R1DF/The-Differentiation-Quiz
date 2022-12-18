# Imports
import toml

# Language Pack class
class LanguagePack:
    def __init__(self, path):
        self.data = toml.load(path)

    def section_get(self, section):
        return self.data[section]
