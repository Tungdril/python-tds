import os

def read(currentWave):

    path = os.getcwd() + "/assets/waves.txt"

    # open the file
    file = open(path, "r")

    # read content of line corresponding to the current wave, remove the newline character
    lineContents = file.readlines()[currentWave].replace("\n", "")

    toBeSpawned = []

    # split the line into a list of strings, append it to the toBeSpawned list
    toBeSpawned.append(lineContents.split(";"))

    # close the file
    file.close()

    # flatten the list, I'm not sure why it's even nested
    flatList = sum(toBeSpawned, [])

    return flatList