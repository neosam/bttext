def readTextfile(filename):
    texts = {}
    textFile = file(filename + "/texts")
    while True:
        try:
            insertKey, insertValue = textFile.readline().split(": ", 2)
            texts[insertKey] = insertValue.replace("\n", "")
        except:
            break
    return texts

def readMapFlags(filename):
    mapFlags = {}

    flagFile = file(filename + "/mapFlags")
    while True:
        try:
            line = flagFile.readline()
            line = line.replace("\n", "")
            newFlag = line.split(",")
            flagContains = []
            for i in range(1, 5):
                flagContains.append(int(newFlag[i]))
            mapFlags[newFlag[0]] = flagContains
        except:
            break
    return mapFlags

def comparePlayerWithFlag(flagname, mapFlags, theWorld):
    try:
        playerPos = theWorld.getPlayerPos()
        goal = mapFlags[flagname]

        if (playerPos[0][0] == goal[0]) &\
               (playerPos[0][1] == goal[1]) &\
               (playerPos[1][0] == goal[2]) &\
               (playerPos[1][1] == goal[3]):
                return True
        return False
    except:
        file("Huhu", "w").write("ERROR")

def setPlayerPosFromFlag(flagname, mapFlags, theWorld):
    goal = mapFlags[flagname]
    theWorld.player.pos[0] = goal[0]
    theWorld.player.pos[1] = goal[1]
