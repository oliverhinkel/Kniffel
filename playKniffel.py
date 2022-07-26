from kniffelPlayer import Player
from kniffelGame import Game
from click import confirm


# Spielerinstanzen erstellen
def initPlayers():
    print("\nSpielfeld wird aufgebaut..", end="")
    players = []
    pNames = []
    pCount = 0

    # Spielerzahl angeben
    while True:

        try:
            pCount = int(input("\nWie viele Spieler? "))

            if confirm("Korrekte Antwort?") and pCount > 0:
                break
            else:
                print("Dann nochmal..\n")

        except:
            print("\nKeine Zahl eingegeben, bitte erneut..\n")

    # Spielernamen angeben
    while True:

        try:

            for i in range(0, pCount):
                pNames.append(str(input(f"\nName von Spieler {i+1}? ")))

            if confirm("\nKorrekte Antwort?"):
                print()
                break
            else:
                pNames.clear()
                print("Dann nochmal..\n")

        except Exception as e:
            print(f"Fehler: {e}")

    # Spielernamen printen vor Beginn des Spiels
    for i in range(0, pCount):
        print(
            f"Name Spieler {i+1} = {pNames[i]}", end=f"{' | ' if i<pCount-1 else ''}",
        )
    print("\n")
    players = [Player(i) for i in pNames]

    return players, pCount


players, pCount = initPlayers()
NewGame = Game(players, pCount)
