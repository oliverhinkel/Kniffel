import random
import easygui as g
import os
from kniffelPlayer import Player

dirname = os.path.dirname(__file__)
helpDir = os.path.join(dirname, "extras/kniffelHelp.txt")


class Game(Player):
    def __init__(self, impPlayers, playerCount):
        self.running = False
        self.players = impPlayers
        self.pCount = playerCount
        self.classes = (
            "Augenzahl",
            "3er Pasch (alle Augen zählen)",
            "4er Pasch (alle Augen zählen)",
            "Full House",
            "Kleine Straße",
            "Große Straße",
            "Kniffel",
            "Chance",
        )
        self.run()

    def wuerfeln(self, length=5):
        wuerfel = []
        wuerfel.append([random.randint(1, 6) for i in range(0, length)])

        return wuerfel[0]

    def wuerfelArt(self, zahlenInp):
        classes = (
            "A",  # Augenzahl
            "3P",  # 3er Pasch
            "4P",  # 4er Pasch
            "F",  # Full House
            "KS",  # Kleine Straße
            "GS",  # Große Straße
            "K",  # Kniffel
            "C",  # Chance
        )
        classCheck = [0, 0, 0, 0, 0, 0, 0, 0]
        classDict = dict(zip(classes, classCheck))
        try:
            w1, w2, w3, w4, w5, w5 = zahlenInp
            zahlen = zahlenInp
        except:
            print("Fehler bei Zahlenspeicherung in Würfelart")
            return None

        for l in range(1, 7):
            for i in range(0, 5):  # 1. Stelle i
                for j in range(0, 5):  # 2. Stelle j
                    if j != i:
                        for k in range(0, 5):  # 3. Stelle k
                            if k != j and k != i:
                                # 3er Pasch
                                # if
                                #   pass
                                for m in range(0, 5):  # 4. Stelle m
                                    if m != j and m != i and m != k:
                                        for n in range(0, 5):  # 5. Stelle n
                                            if n != j and n != i and n != k and n != m:
                                                pass
                                # Vergleiche

        pass

    def zahlenStr(self, inp):
        # Würfelzahlen aus Array als String mit Leerzeichen zurückgeben
        strZahlen = ""
        for i in range(0, len(inp)):
            if i < (len(inp) - 1):
                strZahlen += "[" + str(inp[i]) + "]" + " - "
            else:
                strZahlen += "[" + str(inp[i]) + "]"
        return strZahlen

    def showHelp(self):
        if g.boolbox(
            msg="Möchtest du die Regeln vor deinem Zug anschauen?",
            title="Regelwerk",
            choices=["Ja", "Nein"],
        ):
            file = open(helpDir, "r", encoding="utf-8")
            helpText = file.readlines()
            file.close()
            g.codebox("SPIELREGELN VON KNIFFEL", "Regelwerk", helpText)
        else:
            pass

    def spielzug(self, player, pName):

        """
        Die wichtigste Methode, hier wird jeder Spielzug durchgeführt
        """
        spielzugEnde = False
        spielzugZahlen = []
        spielzugSumme = 0
        print(f"\n--------| SPIELER*IN: {pName.upper()} |--------")

        # For Schleife über die 3 Würfelrunden die man hat in einem Spielzug
        for j in range(0, 3):
            print(f"\n----- Würfel {j+1} -----")

            # If schaut ob erstes Würfeln dann immer 5 Würfel, oder ob erneutes Würfeln dann sind es (5 - Anzahl gespeicherter Würfel)
            if j == 0:
                self.showHelp()
                g.msgbox(msg=f"{pName} ist am Zug", ok_button="Würfeln")
                zahlen = self.wuerfeln()  # Zahlen würfeln (immer 5 in erster Runde)
            else:

                if j < 2:  # If damit im Text entweder Züge oder Zug steht
                    g.msgbox(
                        msg=f"Du hast noch {3-j} Züge übrig {pName}",
                        ok_button="Erneut Würfeln",
                    )
                else:  # Else für Züge oder Zug im Text
                    g.msgbox(
                        msg=f"Das ist dein letzter Zug {pName}",
                        ok_button="Erneut Würfeln",
                    )

                # Zahlen würfeln
                zahlen.extend(  # Nach erstem durchlauf sind die Anzahl von neuen Würfel = (5 - Anzahl gespeicherte Würfel)
                    self.wuerfeln(5 - len(zahlen))
                )

            # Entscheidung von erster Auswahl und zweiter Auswahl
            if j < 2:
                print("Zahlen vor Auswahl:", self.zahlenStr(zahlen))

                # While Schleife, die die Auswahl steuert, abbruch sobald mehrere ausgewählt oder (auch Spielzugende) alle ausgewählt/abbruch der Auswahl
                while True:
                    behalten = g.multchoicebox(  # Auswahlbox bei Runde 1 und 2
                        msg=f"Deine Würfel: {self.zahlenStr(zahlen)}\nWelche Würfel sollen behaltet werden? ",
                        title="--Würfelauswahl Menü--",
                        choices=zahlen,
                        preselect=None,
                    )

                    # If benötigt, weil bei keiner Auswahl oder Abbruch None zurückkommt oder alle ausgewählt sein können
                    if behalten is not None and len(behalten) < len(zahlen):
                        behalten = [int(x) for x in behalten]

                        # Fragebox, ob korrekte Auswahl getroffen wurde, bei ja -> aus Auswahlfrage, bei nein -> in Schleife bleiben
                        if g.ccbox(msg=f"Auswahl korrekt? {self.zahlenStr(behalten)}"):
                            break  # Spieler ist mit Auswahl zufrieden
                        else:
                            pass  # Spieler will Auswahl ändern
                    # Bei Cancel in Auswahlmenü
                    elif behalten == None:

                        if g.ccbox(
                            msg=f"Bei Abbruch/keiner Auswahl werden alle behalten: {self.zahlenStr(zahlen)}"
                        ):
                            break  # Spieler ist mit Auswahl zufrieden
                        else:
                            pass  # Spieler will Auswahl ändern
                    # Bei Auswahl von allen Zahlen
                    else:
                        if g.ccbox(
                            msg=f"Möchtest du alle behalten?: {self.zahlenStr(zahlen)}"
                        ):
                            break  # Spieler ist mit Auswahl zufrieden
                        else:
                            pass  # Spieler will Auswahl ändern

            # Bedingung ob entweder alles behalten wurde oder schon dreimal gewürfelt wurde
            if behalten == None or j == 2 or len(behalten) == len(zahlen):
                spielzugEnde = True
                spielzugZahlen = zahlen
            else:
                zahlen = behalten
                print(f"Behaltene Zahlen:", self.zahlenStr(behalten))

            # Spielende Box
            if spielzugEnde:
                spielzugZahlen = zahlen[:]
                g.msgbox(
                    f"Das Endergebnis dieses Spielzugs ist: {self.zahlenStr(spielzugZahlen)}\nSpielzug von {pName} beendet"
                )
                print("Die endgültigen Zahlen:", self.zahlenStr(zahlen))
                break

        spielzugSumme = sum(spielzugZahlen)
        return spielzugZahlen, spielzugSumme

    def run(self):
        """
        Methode, die das Spiel startet/verwaltet
        """
        print("----| Spiel wird gestartet |----")
        self.running = True

        while self.running:  # Schleife die Spiel bis Ende laufen lässt
            for i in range(0, 13):  # Die Maximal 13 möglichen Spielzüge
                for i in range(0, self.pCount):
                    self.spielzug(self.players[i], self.players[i].spielerName)
                self.running = False
            pass
