import easygui as g


class Player:
    def __init__(self, pName):
        self.oberePunkte = [[[], [], [], [], [], []], [[], [], [], [], [], []]]
        self.unterePunkte = [[[], [], [], [], [], [], []], [[], [], [], [], [], [], []]]
        self.bonusPunkte = False
        self.spielerName = pName
        self.gesamtPunkte = 0
        
    def sayName(self):
        return self.spielerName

    # Obere Punkte hinzufügen
    def addOP(self, points, reihe):
        self.oberePunkte[0][reihe].append(points)

    def bpChecker(self):
        if sum(self.oberePunkte) >= 63:
            self.bonusPunkte = True

    def getPoints(self):
        op = sum(self.oberePunkte)
        up = sum(self.unterePunkte)
        bp = 0
        if self.bonusPunkte:
            bp = 35

        currPoints = op + up + bp

        return currPoints

    # Spezial Würfel berechnen
    def add3Pasch(self, points, specialNr):
        sumP = sum(points)
        self.unterePunkte[0][specialNr].append(sumP)

    def add4Pasch(self, points, specialNr):
        sumP = sum(points)
        self.unterePunkte[1][specialNr].append(sumP)

    def addFullH(self, specialNr):
        self.unterePunkte[2][specialNr].append(25)

    def addKlStr(self, specialNr):
        self.unterePunkte[3][specialNr].append(30)

    def addGrStr(self, specialNr):
        self.unterePunkte[4][specialNr].append(40)

    def addKNIFFEL(self, specialNr):
        self.unterePunkte[5][specialNr].append(50)

    def addChance(self, points, specialNr):
        sumP = sum(points)
        self.unterePunkte[6][specialNr].append(sumP)
