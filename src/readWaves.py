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

    #print(toBeSpawned)

    # close the file
    file.close()

    return toBeSpawned