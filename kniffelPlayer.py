import easygui as g


class Player:
    def __init__(self, pName):
        self.oberePunkte = [[0], [0], [0], [0], [0], [0]]
        self.unterePunkte = [[0], [0], [0], [0], [0], [0], [0]]
        # Classes erste innere Liste ist Obere Punkte und die andere untere Punkte
        self.classesUsed = [[[0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0]]]
        self.bonusPunkte = False
        self.spielerName = pName
        self.gesamtPunkte = 0

    def sayName(self):
        return self.spielerName

    def checkPossibleMove(self, inpDic):
        pass

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
    def add3Pasch(self, points):
        sumP = sum(points)
        self.unterePunkte[0].append(sumP)

    def add4Pasch(self, points):
        sumP = sum(points)
        self.unterePunkte[1].append(sumP)

    def addFullH(self):
        self.unterePunkte[2].append(25)

    def addKlStr(self):
        self.unterePunkte[3].append(30)

    def addGrStr(self):
        self.unterePunkte[4].append(40)

    def addKNIFFEL(self):
        self.unterePunkte[5].append(50)

    def addChance(self, points):
        sumP = sum(points)
        self.unterePunkte[6].append(sumP)
