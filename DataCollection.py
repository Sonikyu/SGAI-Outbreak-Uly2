class DataCollection():
    def __init__(self, starting_zombies, starting_humans):
        self.dataList = []
        self.numStartingZombies = starting_zombies
        self.numStartingHumans = starting_humans
        self.numType1Cured = 0 # these are attempts
        self.numType2Cured = 0
        self.numType3Cured = 0
        self.numType1Success = 0
        self.numType2Success = 0
        self.numType3Success = 0
        self.numType1Killed = 0
        self.numType2Killed = 0
        self.numType3Killed = 0
        self.numPeopleTurnedToZombies = 0
        self.numBiteAttempts = 0
        self.didWin = False
        self.totalMoves = 0
        self.totalScore = 0

    def addMove(self, step_num, zombies, humans, move, zombieType="N/A"):
        obj = {
            "step": step_num,
            "# Zombies": zombies,
            "# Humans": humans,
            "Move": move,
            "Enemy Cured/Killed": zombieType
        }
        self.dataList.append(obj)
    def print_attributes (self):
        string = f"""
        Data List: {self.dataList}
        Win: {self.didWin}
        Starting Zombies: {self.numStartingZombies}
        Starting Humans: {self.numStartingHumans}
        Score: {self.totalScore}
        Total Moves: {self.totalMoves}
        Num People Turned to Zombies: {self.numPeopleTurnedToZombies}
        Num Bite Attempts: {self.numBiteAttempts}
        Type 1 Cured Attempts: {self.numType1Cured}
        Type 2 Cured Attempts: {self.numType2Cured}
        Type 3 Cured Attempts: {self.numType3Cured}
        Type 1 Cured Success: {self.numType1Success}
        Type 2 Cured Success: {self.numType2Success}
        Type 3 Cured Success: {self.numType3Success}
        Type 1 Killed: {self.numType1Killed}
        Type 2 Killed: {self.numType2Killed}
        Type 3 Killed: {self.numType3Killed}"""
        print(string)
        with open('LatestGameData.txt', "w") as f:
            f.write(string)
