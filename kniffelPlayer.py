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
        self.helper = [1, 1]  # helper[0]=Help Menü | helper[1]=Nachfragen

    def getPoints(self):
        oberePunkteInt = [x for x in self.oberePunkte if type(x) == int]
        unterePunkteInt = [x for x in self.unterePunkte if type(x) == int]
        op = sum(oberePunkteInt)
        up = sum(unterePunkteInt)
        bp = 0

        if op >= 63:
            self.bonusPunkte = True
        if self.bonusPunkte:
            bp = 35
            currPoints = op + up + bp
        else:
            currPoints = op + up

        return currPoints

    # Obere Punkte hinzufügen
    def addOP(self, points, reihe):
        self.oberePunkte[reihe] = points
        self.classesUsed[0][reihe][0] = 1

    # Spezial Würfel berechnen
    def addFullH(self):
        self.unterePunkte[2] = 25
        return 25

    def addKlStr(self):
        self.unterePunkte[3] = 30
        return 30

    def addGrStr(self):
        self.unterePunkte[4] = 40
        return 40

    def addKNIFFEL(self):
        self.unterePunkte[5] = 50
        return 50

    def addUP(self, i, points):
        self.unterePunkte[i] = points

