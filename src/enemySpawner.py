import os
import game

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

def main(currentWave, screen):

    spawnedEnemies = []

    #https://stackoverflow.com/questions/65511222/how-do-i-spawn-multiple-enemies-in-pygame
    #https://stackoverflow.com/questions/64530620/how-to-spawn-multiple-enemies-in-pygame

    # TODO implement this correctly
    
    #[0]: amountLight, [1]: typeLight, [2]: amountHeavy, [3]: typeHeavy, [4]: amountFast, [5]: typeFast, [6]: amountBoss, [7]: typeBoss
    toBeSpawned = read(currentWave)

    i = int(toBeSpawned[0][0])

    print(toBeSpawned[0][1])

    for j in range(0, i):
        pos = (100+(j*50), 100)

        listEnemy = game.Enemy(screen, pos, toBeSpawned[0][1])
        
        game.enemyList.append(listEnemy)


    #print("EnemySpawner:", spawnedEnemies)

