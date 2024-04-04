# Imports
from threading import Timer

def periodic_prompt(seconds):
    """
    Prints a statement periodically after time given in seconds
    """
    global counter

    print(f"Hello number {counter}")
    counter += 1
    Timer(seconds, periodic_prompt, [seconds]).start()

    
    

if __name__ == "__main__":
    counter = 1
    periodic_prompt(3)

