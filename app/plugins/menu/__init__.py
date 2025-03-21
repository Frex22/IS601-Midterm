#menu to display all possible commands
from app.commands import Command
import logging
class MenuCommand(Command):
    def __init__(self, command_handler):
        self.command_handler = command_handler

    def execute(self):
        """
        This method executes the menu command
        """
        print("Available Commands:")
        for command_name in self.command_handler.commands:
            print(f"-{command_name}")
        logging.info("Menu Command Executed")

