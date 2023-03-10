"""
Interfaces (in this context) are meant to work as CLI "menu" screens.
"""


# Base
class InterfaceCL:
    def __init__(self, master, language_section_name):
        self.master = master  # the App object that is linked to the interface
        self.configurations = master.configurations
        self.language_pack = master.language_pack
        self.language_section = self.language_pack.menu_get(language_section_name)
        self.continued = True  # Set to false and get to end of loop

        self.load_interface()

    def load_interface(self):
        pass  # Overridden

