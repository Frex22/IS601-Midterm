from app.commands import Command
from app.history import HistoryManager
import logging
def get_float (prompt):
    """
    Helper function to get valid value from float"""
    while True:
        try:
            value = float(input(prompt))
            logging.info(f"Value entered: {value}")
            return value
        except ValueError:
            logging.warning("Invalid Value. Please Try Again.")
            print("Invalid Value. Please Try Again.")

class SubCommand(Command):
    def execute(self):
        """ 
        This method executes the sub command
        """
        logging.info("Executing Sub Command")
        a = get_float("Enter first number: ")
        b = get_float("Enter second number: ")
        result = a - b
        logging.info(f"Subtraction Performed: {a} - {b} = {result}")
        print(f"Result: {a} - {b} = {a - b}")

        history_manager = HistoryManager()
        history_manager.add_calculation('sub', [a, b], result)
        history_manager.save_history()

