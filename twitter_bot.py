# Imports
import os
from time import sleep
from threading import Timer
from api_functions import connect_to_twitter, post_tweet

def periodic_prompt(seconds):
    """
    Prints a statement periodically after time given in seconds
    """
    global counter

    print(f"Hello number {counter}")
    counter += 1
    Timer(seconds, periodic_prompt, [seconds]).start()

    
    

if __name__ == "__main__":

    working_flag = 1
    while working_flag:
        response = input("c - start counter\nt - connect to twitter\np - post a tweet\nq - quit application\nChoose option: ")
        if response == "c":
            working_flag = 0
            counter = 1
            seconds = 1
            periodic_prompt(seconds)
            sleep(seconds+4)
        elif response == "t":
            autohrized_connection = connect_to_twitter()
        elif response == "p":
            text = input("Write your twitt and press enter:\n")
            post_tweet(autohrized_connection, text)
        elif response == "q":
            working_flag = 0
        else:
            print("\nUnknown command!\n")

    print("\nThanks for attention!\n")


