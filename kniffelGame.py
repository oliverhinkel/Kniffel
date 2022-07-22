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
            "Streichen",
        )
        self.run()

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

    def zahlenStr(self, inp):
        # Würfelzahlen aus Array als String mit Leerzeichen zurückgeben
        strZahlen = ""
        for i in range(0, len(inp)):
            if i < (len(inp) - 1):
                strZahlen += "[" + str(inp[i]) + "]" + " - "
            else:
                strZahlen += "[" + str(inp[i]) + "]"
        return strZahlen

    def wuerfeln(self, length=5):
        wuerfel = []
        wuerfel.append([random.randint(1, 6) for i in range(0, length)])

        return wuerfel[0]

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

    def spielzug(self, pName):

        """
        Die wichtigste Methode, hier wird jeder Spielzug durchgeführt
        """
        spielzugEnde = False
        spielzugZahlen = []
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

        return spielzugZahlen

    def wuerfelArt(self, zahlenInp):
        classCheck = [0, 0, 0, 0, 0, 0, 0, 0]
        classes = (
            "P",  # Augenzahl (hier als Paare um aus 3er Pasch und Paar ein Full House zu finden)
            "3P",  # 3er Pasch
            "4P",  # 4er Pasch
            "F",  # Full House
            "KS",  # Kleine Straße
            "GS",  # Große Straße
            "K",  # Kniffel
            "C",  # Chance
            "ST",  # Streichen
        )
        classDict = dict(zip(classes, classCheck))
        wuerfel = zahlenInp
        wuerfel.sort()
        paare = []
        for l in range(1, 7):

            for i in range(0, 5):  # 1. Stelle i

                for j in range(0, 5):  # 2. Stelle j
                    if j != i:

                        for k in range(0, 5):  # 3. Stelle k
                            if k != j and k != i:

                                # 3er Pasch ----------------------------------
                                if (
                                    wuerfel[i] == wuerfel[j] == wuerfel[k]
                                    and classDict["3P"] == 0
                                ):
                                    # Speichert die 3er Paschzahl in classCheck ab
                                    classCheck[1] = wuerfel[i]
                                    # Setzt 3er Pasch von 0 auf 1 (False -> True)
                                    classDict["3P"] = 1

                                # Paare für Fullhouse schauen ----------------------
                                if (
                                    wuerfel[i] == wuerfel[j]  # Beide Würfel vergleichen
                                    # Schauen ob bereits ein Eintrag in classDict gemacht wurde <2 weil zwei Paare möglich sind
                                    and classDict["P"] < 2
                                    # Schaut ob erstes gefundenes Paar ungleich dem Würfel ist
                                    and classCheck[0] != wuerfel[i]
                                    # Schaut ob aktueller Würfel nicht die Zahl des Pasch ist
                                    and classCheck[1] != wuerfel[i]
                                    # Erst ab l>2 anfangen nach Paaren zu suchen, weil sonst Paare vor Pasche gefunden werden und doppelt vorkommen
                                    and l > 1
                                ):
                                    # Speichert erstes paar in classCheck ab
                                    classCheck[0] = wuerfel[i]
                                    # Speichert Paare in Liste, damit am Ende alle Paare in classCheck eingefügt werden können
                                    paare.append(wuerfel[i])
                                    # classDict += weil es hierbei zwei mögliche Paare gibt und nicht nur eins wie bei 3er oder 4er Pasch
                                    classDict["P"] += 1

                                for m in range(0, 5):  # 4. Stelle m

                                    if m != j and m != i and m != k:
                                        # 4er Pasch ----------------------------------
                                        if (
                                            wuerfel[i]
                                            == wuerfel[j]
                                            == wuerfel[k]
                                            == wuerfel[m]
                                            and classDict["4P"] == 0
                                        ):
                                            # Speichert die 4er Paschzahl in classCheck ab
                                            classCheck[2] = wuerfel[i]
                                            # Setzt 4er Pasch von 0 auf 1 (False -> True)
                                            classDict["4P"] = 1
                                        # Kleine Straße ------------------------------
                                        if (
                                            [
                                                wuerfel[i],
                                                wuerfel[j],
                                                wuerfel[k],
                                                wuerfel[m],
                                            ]
                                            == [1, 2, 3, 4]
                                            or [
                                                wuerfel[i],
                                                wuerfel[j],
                                                wuerfel[k],
                                                wuerfel[m],
                                            ]
                                            == [2, 3, 4, 5]
                                            or [
                                                wuerfel[i],
                                                wuerfel[j],
                                                wuerfel[k],
                                                wuerfel[m],
                                            ]
                                            == [3, 4, 5, 6]
                                            and classDict["KS"] != 1
                                        ):
                                            classDict["KS"] = 1

                                        for n in range(0, 5):  # 5. Stelle n

                                            if n != j and n != i and n != k and n != m:
                                                # Kniffel ----------------------------------
                                                if (
                                                    wuerfel[i]
                                                    == wuerfel[j]
                                                    == wuerfel[k]
                                                    == wuerfel[m]
                                                    == wuerfel[n]
                                                    and classDict["K"] == 0
                                                ):
                                                    # Setzt Kniffel von 0 auf 1 (False -> True)
                                                    classDict["K"] = 1

                                            # Große Straße ------------------------------
                                            if (
                                                [
                                                    wuerfel[i],
                                                    wuerfel[j],
                                                    wuerfel[k],
                                                    wuerfel[m],
                                                    wuerfel[n],
                                                ]
                                                == [1, 2, 3, 4, 5]
                                                or [
                                                    wuerfel[i],
                                                    wuerfel[j],
                                                    wuerfel[k],
                                                    wuerfel[m],
                                                    wuerfel[n],
                                                ]
                                                == [2, 3, 4, 5, 6]
                                                and classDict["GS"] != 1
                                            ):
                                                classDict["GS"] = 1

        # Full House ----------------------------------
        if classDict["3P"] == 1 and classDict["P"] >= 1:
            classDict["F"] = 1

        # Chance ----------------------------------
        if (
            classDict["3P"] == 0
            and classDict["4P"] == 0
            and classDict["F"] == 0
            and classDict["KS"] == 0
            and classDict["GS"] == 0
            and classDict["K"] == 0
        ):
            classDict["C"] = 1

        classCheck[0] = paare
        print(
            f"3er Pasch mit Zahl: {classCheck[1]}\n" if classDict["3P"] == 1 else "\n",
            f"4er Pasch mit Zahl: {classCheck[2]}\n" if classDict["4P"] == 1 else "\n",
            f"Full House\n" if classDict["F"] == 1 else "\n",
            f"Kleine Straße\n" if classDict["KS"] == 1 else "\n",
            f"Große Straße\n" if classDict["GS"] == 1 else "\n",
            f"KNIFFEL!!!" if classDict["K"] == 1 else "",
            f"Chance" if classDict["C"] == 1 else "",
        )
        return wuerfel, classDict

    def auswahl(self, inpZahlen, inpDict):
        wuerfel = inpZahlen
        classDict = inpDict

        g.choicebox(msg="Treffe deine Entscheidung für diesen Spielzug")

    def run(self):
        """
        Methode, die das Spiel startet/verwaltet
        """
        print("----| Spiel wird gestartet |----")
        self.running = True

        while self.running:  # Schleife die Spiel bis Ende laufen lässt
            for i in range(0, 13):  # Die Maximal 13 möglichen Spielzüge
                for i in range(0, self.pCount):
                    endzahlen = self.spielzug(
                        self.players[i], self.players[i].spielerName
                    )
                self.running = False
            pass

