# Imports
from threading import Timer

def periodic_prompt(seconds):
    """
    Prints a statement periodically after time given in seconds
    """
    print("Hello")
    Timer(seconds, periodic_prompt(seconds)).start()

periodic_prompt(1)

