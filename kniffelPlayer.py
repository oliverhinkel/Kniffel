import easygui as g


class Player:
    def __init__(self, pName):
        self.oberePunkte = [0, 0, 0, 0, 0, 0]
        self.unterePunkte = [0, 0, 0, 0, 0, 0, 0]
        # Classes erste innere Liste ist Obere Punkte und die andere untere Punkte
        self.classesUsed = [
            [[0], [0], [0], [0], [0], [0]],
            [[0], [0], [0], [0], [0], [0], [0]],
        ]
        self.bonusPunkte = False
        self.spielerName = pName
        self.gesamtPunkte = 0

    # Obere Punkte hinzufügen
    def addOP(self, points, reihe):
        self.oberePunkte[reihe] = points
        self.classesUsed[0][reihe][0] = 1

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
        else:
            currPoints = op + up

        return currPoints

    # Spezial Würfel berechnen
    def add3Pasch(self, reihe, points):
        sumP = sum(points)
        self.unterePunkte[0].append(sumP)
        self.classesUsed[1][reihe][0] = 1

    def add4Pasch(self, reihe, points):
        sumP = sum(points)
        self.unterePunkte[1].append(sumP)
        self.classesUsed[1][reihe][0] = 1

    def addFullH(self, reihe):
        self.unterePunkte[2].append(25)
        self.classesUsed[1][reihe][0] = 1

    def addKlStr(self, reihe):
        self.unterePunkte[3].append(30)
        self.classesUsed[1][reihe][0] = 1

    def addGrStr(self, reihe):
        self.unterePunkte[4].append(40)
        self.classesUsed[1][reihe][0] = 1

    def addKNIFFEL(self, reihe):
        self.unterePunkte[5].append(50)
        self.classesUsed[1][reihe][0] = 1

    def addChance(self, reihe, points):
        sumP = sum(points)
        self.unterePunkte[6].append(sumP)
        self.classesUsed[1][reihe][0] = 1
