# Imports
import os
from time import sleep
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

    response = ""
    while response != "c":
        response = input("c - start counter\ns - print secret\nYour answer: ")
        if response == "c":
            counter = 1
            seconds = 1
            periodic_prompt(seconds)
            sleep(seconds+4)
        elif response == "s":
            api_file = open("secrets/api_key.txt")
            print(f"api_key: {api_file.read()}")
            api_secret_file = open("secrets/api_key_secret.txt")
            print(f"api_key_secret: {api_secret_file.read()}")


