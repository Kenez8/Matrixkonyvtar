#Kenéz Máté B6ONGN 2025.11.30.

from datetime import datetime
import os

class Matrix:
    def __init__(self, sor, oszlop, adatok=None):
        self.sor = int(sor)
        self.oszlop = int(oszlop)
        self.adatok = adatok

    def __str__(self):
        def fmt(x):
        # minden floatot normálisan formázunk
            if isinstance(x, float):
                s = f"{x:.3f}"   # 3 tizedesjegy
                if "." in s:
                    s = s.rstrip("0").rstrip(".")  # felesleges nullák levágása
                return s
            return str(x)    
        
        # Legnagyobb elem hossza
        max_hossz = 0
        for sor in self.adatok:
            for elem in sor:
                hossz = len(fmt(elem))
                if hossz > max_hossz:
                    max_hossz = hossz

        # Minden számot ugyanakkora szélességgel írunk ki
        szoveg = []
        for sor in self.adatok:
            sor_ki = " ".join(f"{fmt(elem):>{max_hossz}}" for elem in sor)
            szoveg.append(sor_ki)
        return "\n".join(szoveg)

    def fajlba_ir(self, fajlnev):
        """A mátrixot .csv-be írja a kívánt formátumban."""
        with open(fajlnev, "w") as f:
            # fejlécként dátum + verzió
            f.write(f"//{datetime.now().strftime('%Y.%m.%d')} v1\n")
            # méretek
            f.write(f"{self.sor},{self.oszlop}\n")
            # mátrix adatok
            for sor in self.adatok:
                f.write(",".join(str(x) for x in sor) + "\n")

def fajlbol_olvas(fajlnev):
    with open("matrixok/" + fajlnev, "r") as f:
        # Az első sort kihagyom, mert az komment
        next(f)
        # A második sor a méreteket tárolja
        sorok = next(f).strip()
        meret = sorok.split(",")
        sor = int(meret[0])
        oszlop = int(meret[1])
        
        # A tartalmi adatok beolvasása
        adatok = []
        for _ in range(sor):
            adatsor_szoveg = next(f).strip()
            darabok = adatsor_szoveg.split(",")
            
            # konvertáljuk számmá
            egy_sor = []
            for x in darabok:
                egy_sor.append(float(x))
            
            adatok.append(egy_sor)

    return Matrix(sor, oszlop, adatok)

def torol_matrix(fajlnev):
    """Ez a függvény felelős a mátrixok törlésének logikájáért."""
    os.remove("matrixok/" + fajlnev)

def modosit_matrix(matrix, fajlnev):
    """Mátrix elem módosítása biztonságos hibakezeléssel."""
    while True:
        try:
            s = int(input(f"Sor index (0–{matrix.sor-1}): "))
            if s < 0 or s >= matrix.sor:
                print("Hiba: ilyen sor nem létezik.")
                continue

            o = int(input(f"Oszlop index (0–{matrix.oszlop-1}): "))
            if o < 0 or o >= matrix.oszlop:
                print("Hiba: ilyen oszlop nem létezik.")
                continue

            ertek = input("Új érték (float): ").strip()
            uj = float(ertek)

            # módosítás
            matrix.adatok[s][o] = uj

            # mentés
            matrix.fajlba_ir("matrixok/" + fajlnev)

            print("Elem módosítva és mentve.")
            return

        except ValueError:
            print("Hiba: számot adj meg!")
        except Exception as e:
            print(f"Váratlan hiba: {e}")

def letrehoz_egyseges():
    nev = input("Adj nevet a mátrixnak (pl. A): ").strip().upper()
    fajlnev = "matrixok/" + nev + ".csv"

    meret = int(input("Méret (n): "))

    # Egységmátrix adatai
    adatok = []
    for i in range(meret):
        sor = []
        for j in range(meret):
            if i == j:
                sor.append(1)
            else:
                sor.append(0)
        adatok.append(sor)

    matrix = Matrix(meret, meret, adatok)
    matrix.fajlba_ir(fajlnev)

    print(f"{nev} egységmátrix létrehozva és mentve.")

def letrehoz_kezi():
    nev = input("Adj nevet a mátrixnak (pl. B): ").strip().upper()
    fajlnev = "matrixok/" + nev + ".csv"

    try:
        sor = int(input("Sorok száma: "))
        oszlop = int(input("Oszlopok száma: "))
    except ValueError:
        print("A sorok és oszlopok számának egész számnak kell lennie!")
        return

    adatok = []

    for i in range(sor):
        print(f"{i}. sor értékei:")
        egy_sor = []

        for j in range(oszlop):
            while True:
                ertek = input(f"  [{i},{j}] = ").strip()

                try:
                    szam = float(ertek)   # ← FLOAT érték elfogadása
                    egy_sor.append(szam)
                    break
                except ValueError:
                    print("Hiba: az értéknek számnak (float) kell lennie!")

        adatok.append(egy_sor)

    matrix = Matrix(sor, oszlop, adatok)
    matrix.fajlba_ir(fajlnev)

    print(f"{nev} mátrix sikeresen létrehozva és mentve.")
