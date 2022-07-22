import random
import easygui as g
import os
from kniffelPlayer import Player
from time import sleep
import sys

dirname = os.path.abspath("")
helpDir = os.path.join(dirname, "extras/kniffelHelp.txt")


class Game(Player):
    def __init__(self, impPlayers, playerCount):
        self.running = False
        self.players = impPlayers
        self.pCount = playerCount
        self.classes = (
            "3er Pasch",
            "4er Pasch",
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

    def wuerfelZug(self, pName):

        """Beschreibung:\n
        Der Würfelzug eines Spielers, in dem die Würfel gewürfelt werden und die Auswahl der Würfel (nicht Punktzahl)
        stattfindet
            
        Returns:
            spielzugZahlen(List of Ints): Die Würfelzahlen, die der Spieler hier ausgewählt hat
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
                        title=f"--Würfelauswahl Menü: {pName}--",
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
                print("Die endgültigen Zahlen:", self.zahlenStr(zahlen))
                g.msgbox(
                    f"Die Würfelzahlen dieses Spielzugs sind: {self.zahlenStr(spielzugZahlen)}"
                )
                break

        print("\n--------| WÜRFELN BEENDET |--------\n")
        return spielzugZahlen

    def wuerfelArt(self, zahlenInp):
        """Beschreibung:
        \nBerechnet die Möglichkeiten die die Würfelzahlen anbieten
        ohne zu beachten, was der Spieler bereits ausgefüllt hat.

        Args:
            zahlenInp (List of Ints): Die Würfelzahlen aus dem Spielzug

        Returns:
            ClassDict(Dict): Ein Dictionary das die Möglichkeiten des Spielzugs abgespeichert hat,
            ohne dabei zu beachten, was der Spieler bereits ausgefüllt hat
        """
        classCheck = [0, 0, 0, 0, 0, 0, 0, 0]
        classesWuerfelArt = (
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
        classDict = dict(zip(classesWuerfelArt, classCheck))
        wuerfel = sorted(zahlenInp)
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

        return classDict

    def auswahl(self, playerInp, zahlenInp, inpDict):
        """Beschreibung:\n
        In dieser Methode wird die Auswahl des Spielers gesteuert und seine
        Auswahl wird in sein Logbuch eingetragen.

        Args:
            playerInp (Obj): Der Spieler wird als Object übergeben\n
            zahlenInp (_type_): Die Würfelzahlen aus dem Spielzug\n
            inpDict (_type_): Das Dictionary mit den Möglichkeiten
            der Würfelzahlen aus der 'wuerfelArt' Methode

        Returns:
            Wuerfel(List of Ints): Die Würfelzahlen aus dem Spielzug\n
            Ergebnis(List of 2 Lists of Ints): Aufgeteilt in Ergebnis[0],
            das sind die normalen Ergebnise und Ergebnis[1], die Ergebnisse
            falls ein Spieler ein zweites/n-tes Mal ein Kniffel würfelt
        """
        wuerfel = sorted(zahlenInp)
        classDict = inpDict
        player = playerInp
        print(f"{player.spielerName} wählt Punktzahl aus..")
        # ---------- Variablen für Auswahl ----------
        # Classes Used aus Player Klasse

        antwortIndexNoDK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        doppelkniffel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        augenzahlen = [1, 2, 3, 4, 5, 6]  # Neu
        auswahlAugen = []  # Neu
        auswahlSpecials = []  # Neu
        auswahlDoppelKniffel = []
        classDictKeys = list(classDict)  # Keys von classDict als Liste
        istDoppelkniffel = False
        alleAugenDK = []
        alleSpecialDK = []
        alleDoppelkniffel = []

        if player.classesUsed[1][5][0] >= 1:
            istDoppelkniffel = True

        # ---------- Auswahl vorbereiten ----------
        # Augenzahlen in Auswahl stecken
        for i in range(0, 6):
            alleAugenDK.append(f"Doppelkniffel für Augenzahl: {i+1}")
            for j in range(0, len(wuerfel)):
                if (
                    player.classesUsed[0][i] == [0]
                    and wuerfel[j] == (i + 1)
                    and wuerfel[j] not in auswahlAugen
                ):
                    auswahlAugen.append(i + 1)

            # Doppelkniffel
            if player.classesUsed[0][i] == [0] and istDoppelkniffel:
                auswahlDoppelKniffel.append(f"Doppelkniffel für Augenzahl: {i+1}")

        # Specials in Auswahl stecken
        for i in range(0, len(self.classes) - 1):
            # Specials in alle möglichen Doppelkniffel hinzufügen
            if i != 5:
                alleSpecialDK.append(f"Doppelkniffel für Special: {self.classes[i]}")
            if (
                classDict[classDictKeys[i + 1]] == 1
                and player.classesUsed[1][i][0] == 0
            ):
                auswahlSpecials.append(self.classes[i])
            # Doppelkniffel in Auswahl
            if player.classesUsed[1][i][0] == 0 and istDoppelkniffel and i != 5:
                auswahlDoppelKniffel.append(
                    f"Doppelkniffel für Special: {self.classes[i]}"
                )

        # Doppelkniffel zurücksetzen
        if player.classesUsed[1][5][0] > 1:
            player.classesUsed[1][5][0] = 1

        # ---------- Auswahl ----------
        # Gesamtauswahl
        gesamtauswahl = (
            auswahlAugen + auswahlSpecials + auswahlDoppelKniffel + ["Streichen"]
        )

        while True:
            antwort = g.choicebox(
                msg=f"Treffe deine Entscheidung für diesen Spielzug\n Deine Würfelzahlen sind: {self.zahlenStr(wuerfel)}",
                choices=gesamtauswahl,
                title="Auswahl",
                preselect=0,
            )
            if antwort == None:
                print("Keine gültige Eingabe")
                g.msgbox(
                    msg="Keine gültige Eingabe", title="Fehler", ok_button="Nochmal"
                )
            else:
                break

        # ---------- Auswahl verarbeiten ----------
        # Entweder Index des Spezialwurf nehmen oder Antwort ist Augenzahl oder Antwort ist Doppelkniffel
        antwortIndexSpecials = None
        antwortIndexAugen = None
        antwortIndexKniffel = None

        # Indexsuche von Augenzahl als Antwort
        for i in range(0, 6):
            if antwort == str(i + 1):
                antwortIndexAugen = i
                print(f"Augenzahl {i+1} ausgewählt")

        # Indexsuche von Spezialwürfen als Antwort
        if antwortIndexAugen == None:
            for i in range(0, len(self.classes)):

                if self.classes[i] == antwort and antwort != "Streichen":
                    antwortIndexSpecials = i + 6
                    print(f"{self.classes[i]} ausgewählt")

        # Indexsuche wenn Antwort ein Doppelkniffel ist
        alleDoppelkniffel = alleAugenDK + alleSpecialDK
        if antwortIndexAugen == None:

            for i in range(0, len(alleDoppelkniffel)):

                if antwort == alleDoppelkniffel[i]:
                    doppelkniffel[i] = 1
                    print("Doppelkniffel ausgewählt")

        # Streichen als Antwort
        if antwort == "Streichen":
            antwortIndexNoDK[-1] = 1
            print("Streichen ausgewählt")

        # ---------- Ergebnis Liste erstellen ----------
        for i in range(0, len(antwortIndexNoDK)):
            # If checkt ob obere Punktzahl betroffen (1-6)
            if i < 6:
                # If checkt ob i == Auge
                if i == antwortIndexAugen:
                    antwortIndexNoDK[i] = 1
                    player.classesUsed[0][i][0] = 1

            elif i < 13:
                if i == antwortIndexSpecials:
                    antwortIndexNoDK[i] = 1
                    player.classesUsed[1][i - 6][0] = 1

        # print(ergebnis) # ---- INFO PRINT
        # print(player.classesUsed)
        ergebnis = [antwortIndexNoDK, doppelkniffel]

        return ergebnis

    def berechnePunkte(self, playerInp, zahlenInp, auswahlInp):
        """Beschreibung:\n
        Diese Methode berechnet die Punktzahl und achtet dabei auf verschiedene
        Dinge wie z.B. ob doppelter/n-ter Kniffel gewürfelt wurde oder ob
        der Spieler etwas streicht (dann wird die Streichmethode gerufen)

        Args:
            playerInp (Object Instance): der aktuelle Spieler
            zahlenInp (List of ints): die gewürfelten Zahlen
            auswahlInp (List of 2 Lists of ints): Liste mit Liste[0]=normale Auswahl, Liste[1]=doppelter/n-ter Kniffel
        """
        print("\n-------- ERGEBNIS --------")
        wuerfel = zahlenInp  # Ersetzen mit zahlenInp
        player = playerInp  # Ersetzen mit playerInp
        punktzahl = 0

        # Variablen nach Auswahl normaler Optionen und doppel Kniffel entpacken
        auswahlN = auswahlInp[0]
        auswahlDK = auswahlInp[1]

        # Normale Auswahl in Augenzahl und Spezialwurf Auswahl teilen
        auswahlA = auswahlN[:6]
        auswahlSpe = auswahlN[6:-1]

        # DK Auswahl in Augenzahl und Spezialwurf Auswahl teilen
        auswahlDKA = auswahlDK[:6]
        auswahlDKSPE = auswahlDK[6:]
        dkAugenzahlWahl = True if sum(auswahlDKA) > 0 else False
        dkSpezialWahl = True if sum(auswahlDKSPE) > 0 else False

        # Prüfen nach Art der Auswahl
        # Normal heißt, ohne doppelten/n-fachen Kniffel
        normaleAuswahl = True if sum(auswahlN[:-1]) > 0 else False
        # True wenn Augenzahl gewählt wurde
        augenzahlWahl = True if sum(auswahlA) > 0 else False
        # True wenn Spezialwurf gewählt wurde
        spezialWahl = True if sum(auswahlSpe) > 0 else False
        # Auswahl auf Streichen prüfen
        streichWahl = True if auswahlN[-1] == 1 else False

        if normaleAuswahl and (augenzahlWahl or spezialWahl):
            # Berechnungen mit Augenzahlwahl
            if augenzahlWahl:

                for i in range(0, 6):

                    if auswahlA[i] > 0:
                        # Augenzahl Häufigkeit in Würfelzahlen zählen
                        punktzahl = (wuerfel.count(i + 1)) * (i + 1)
                        # Spieler die Punktzahl gutschreiben
                        player.addOP(punktzahl, i)
            else:

                for i in range(0, len(auswahlSpe)):

                    if auswahlSpe[i] > 0:

                        if i in [
                            0,
                            1,
                            6,
                        ]:  # 3er, 4er Pasch und Chance einfache Punktzahl
                            punktzahl = sum(wuerfel)
                            player.addUP(i, punktzahl)
                        else:
                            if i == 2:
                                punktzahl = player.addFullH()
                            if i == 3:
                                punktzahl = player.addKlStr()
                            if i == 4:
                                punktzahl = player.addGrStr()
                            if i == 5:
                                punktzahl = player.addKNIFFEL()

        elif streichWahl:
            print("Es wird ein Feld gestrichen")
            # Streichwahl Methode aufrufen

        else:
            # Berechnungen für DoppelKniffel
            if dkAugenzahlWahl:

                for i in range(0, 6):

                    if auswahlDKA[i] > 0:
                        # Augenzahl Häufigkeit in Würfelzahlen zählen
                        punktzahl = wuerfel[i] * 5
                        # Spieler die Punktzahl gutschreiben
                        player.addOP(punktzahl, i)
                        player.classesUsed[0][i] = 1
            elif dkSpezialWahl:
                for i in range(0, len(auswahlDKSPE)):

                    if auswahlDKSPE[i] > 0:

                        if i in [
                            0,
                            1,
                            5,
                        ]:  # 3er, 4er Pasch und Chance einfache Punktzahl
                            punktzahl = 6 * 5
                            if i != 5:
                                player.classesUsed[1][i] = 1
                            else:
                                player.classesUsed[1][i + 1] = 1
                            player.addUP(i, punktzahl)
                        else:
                            if i == 2:
                                punktzahl = player.addFullH()
                            if i == 3:
                                punktzahl = player.addKlStr()
                            if i == 4:
                                punktzahl = player.addGrStr()

        # Runden Ergebnis
        print(f"Diese Runde hat {player.spielerName} {punktzahl} Punkte gebracht!")
        player.gesamtPunkte = player.getPoints()
        print("Gesamtpuntzahl:", player.gesamtPunkte)

        g.msgbox(
            msg=f"Diese Runde hat {player.spielerName} {punktzahl} Punkte gebracht!\nAktuelle Gesamtpuntzahl: {player.gesamtPunkte}",
            title=f"Punktzahl {player.spielerName}: {player.gesamtPunkte}",
            ok_button="Weiter",
        )

    def spielzugEnde(self, currSpieler, nextSpieler):
        player = currSpieler
        nPlayer = nextSpieler
        print(f"*****|Spielzug von {player.spielerName} beendet|*****".upper())
        while True:
            ausgabe = g.ccbox(
                msg=f"Spielzug von {player.spielerName} beendet\nAls nächstes ist {nPlayer.spielerName} dran!",
                title="Ende des Spielzugs",
                choices=["Weiterspielen", "Spiel beenden"],
            )
            if ausgabe:
                print(f"Nächste Runde startet, {nPlayer.spielerName} mach dich bereit!")
                break
            else:
                print(f"{player.spielerName} möchte das Spiel vorzeitig beenden..")
                endgame = g.ccbox(msg="Wirklich beenden?", choices=["Ja", "Nein"])
                if endgame:
                    print("Das Spiel wird beendet :(")
                    print(
                        "\n##########################################################"
                    )
                    sys.exit()
        print("********************************************************")
        print("********************************************************")

    def run(self):
        """
        Methode, die das Spiel startet/verwaltet.
        Kontrolliert die Ein- und Ausgabeparameter der anderen Methoden.
        """
        print("----| Spiel wird gestartet |----")
        self.running = True

        while self.running:  # Schleife die Spiel bis Ende laufen lässt
            for j in range(0, 2):  # Die Maximal 13 möglichen Spielzüge
                g.msgbox(
                    msg=f"RUNDE {j+1}",
                    title="MITTEILUNG",
                    ok_button=f"Starte Runde {j+1}",
                )

                for i in range(0, self.pCount):  # Ein Spielzug für alle Spieler

                    # Spielzug für Spieler i durchführen und seine Würfelzahlen speichern
                    wuerfelZahlen = self.wuerfelZug(self.players[i].spielerName)

                    # Würfelzahlen + mögliche Würfelarten abspeichern
                    waDict = self.wuerfelArt(zahlenInp=wuerfelZahlen)

                    # Auswahl des Spielers starten
                    awErgebnis = self.auswahl(self.players[i], wuerfelZahlen, waDict)

                    # Punktzahl ausrechnen
                    self.berechnePunkte(self.players[i], wuerfelZahlen, awErgebnis)

                    # Spielzug Ende (optimalerweise letzter Befehl)
                    self.spielzugEnde(
                        self.players[i],
                        self.players[i + 1]
                        if i < (self.pCount - 1) and self.pCount > 1
                        else self.players[0],
                    )

            self.running = False
