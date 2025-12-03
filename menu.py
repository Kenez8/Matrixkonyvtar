#Kenéz Máté B6ONGN 2025.11.30.

import pyconio
from matrix import *
from algoritmusok import *
from muveletek import *

def fomenu():
    while True:
        pyconio.clrscr()
        print('''----------MÁTRIX FŐMENÜ----------
Válassz a menüpontok közül:

1. Új Mátrix létrehozása
2. Mátrixok kezelése
3. Műveletek
4. Algoritmusok
0. Kilépés
---------------------------------''')
        try:
            valasz = int(input("Válassztás: "))
            if valasz < 0 or valasz > 4:
                print("Hiba!: A választás 0 és 4 között kell, hogy legyen.")
                continue
            elif valasz == 1:
                menu1()
            elif valasz == 2:
                menu2()
            elif valasz == 3:
                menu3()
            elif valasz == 4:
                menu4()
            elif valasz == 0:
                kilepes()
                break
        except ValueError:
            print("Hiba!: A bemenetnek számnak kell lennie. (0-4)")
            continue

def menu1():
    """Új mátrix létrehozása"""
    pyconio.clrscr()
    print('''\n---------- MÁTRIX LÉTREHOZÁSA ----------
1. Egységmátrix létrehozása
2. Mátrix megadása kézzel
---------------------------------
.. Vissza | 0. Kilépés
''')
    while True:    
        valasz = input("Választás: ").strip().lower()
        if valasz == "..":
            return
        elif valasz == "0":
            kilepes()
            exit()
        elif valasz == "1":
            letrehoz_egyseges()
        elif valasz == "2":
            letrehoz_kezi()
        else:
            print("Hibás választás! (0-2 vagy ..) ")

def menu2():
    '''Itt tudod modosítani, törölni a korábbi mátrixokat.'''
    pyconio.clrscr()
    while True: 
        print('''\n---------- MÁTRIXOK KEZELÉSE----------
Add meg a mátrix nevét, amit kezelni szeretnél!
---------------------------------
.. Vissza | 0. Kilépés
''')   
        valasz = input("Választás: ").strip().upper()
        if valasz == "..":
            return
        elif valasz == "0":
            kilepes()
            exit()
        else:
            fajlnev = valasz + ".csv"
            try:
                matrix = fajlbol_olvas(fajlnev)
            except FileNotFoundError:
                print(f"Nincs ilyen mátrix: {fajlnev}")
                continue

        while True:
            pyconio.clrscr()
            print(f"MÁTRIX: {valasz}\n")
            print(matrix)
            print('''
-----------------------------
1. Módosítás
2. Törlés
.. Vissza | 0. Kilépés
''')

            muvelet = input("Választás: ").strip()

            if muvelet == "..":
                return
            
            elif valasz == "0":
                kilepes()
                exit()

            elif muvelet == "1":
                modosit_matrix(matrix, fajlnev)
                return   # vissza a MENU2 felső szintjére

            elif muvelet == "2":
                torol_matrix(fajlnev)
                print("Mátrix törölve.")
                return   # vissza a MENU2-be

            else:
                print("Érvénytelen választás.")
                # azonnal visszamegy a ciklus elejére
                continue    

def menu3():
    '''Itt kiválaszthatsz egy mátrixot,
    aztán ki kell választanod mit akarsz vele csinálni.
    
    Ha transzponálni, akkor kiírja az eredményt,
    ha olyan műveletet, amit több mátrixszal kell
    (Mátrix szorzást, összeadás, kivonás), akkor kéri,
    hogy válassz még egy mátrixot. A Skalárral való szorzás
    esetén egy float számot fog elfogadni.
    
    Ezután kiírja az eredményt, ekkor új műveletet kezdhetsz
    a már új mátrixon. Illetve lementheted az eredményt'''
    pyconio.clrscr()
    print("\n------ MŰVELETEK ------\n")

    # 1) Első mátrix kiválasztása
    while True:
        nev1 = input("Add meg a mátrix nevét: ").strip().upper()
        if nev1 == "..":
            return
        fajl1 = nev1 + ".csv"
        try:
            A = fajlbol_olvas(fajl1)
            break
        except FileNotFoundError:
            print("Nincs ilyen mátrix.")

    # 2) Művelet választása
    while True:
        pyconio.clrscr()
        print(f"MÁTRIX: {nev1}\n")
        print(A)
        print('''
-----------------------------
Válassz műveletet:

1. Transzponálás
2. Skalárral szorzás
3. Mátrix + Mátrix
4. Mátrix - Mátrix
5. Mátrix * Mátrix
.. Vissza | 0. Kilépés
''')

        valasz = input("Választás: ").strip()

        if valasz == "..":
            return
        elif valasz == "0":
            kilepes()
            exit()

        # Egymátrixos műveletek 
        elif valasz == "1":
            eredmeny = transzponal(A)

        elif valasz == "2":
            try:
                k = float(input("Skalár: "))
                eredmeny = skalarral_szoroz(A, k)
            except ValueError:
                print("Hibás szám.")
                continue

        # Kétmátrixos műveletek
        elif valasz in ("3", "4", "5"):
            nev2 = input("Második mátrix neve: ").strip().upper()
            fajl2 = nev2 + ".csv"
            try:
                B = fajlbol_olvas(fajl2)
            except FileNotFoundError:
                print("Nincs ilyen mátrix.")
                continue

            if valasz == "3":
                eredmeny = osszead(A, B)
            elif valasz == "4":
                eredmeny = kivon(A, B)
            elif valasz == "5":
                eredmeny = szorzas(A, B)

        else:
            print("Érvénytelen választás.")
            continue

        # 3) Eredmény kiírása
        pyconio.clrscr()
        print("EREDMÉNY:\n")
        print(eredmeny)

        # 4) Mentés opcionálisan
        ment = input("\nMentsem? (i/n): ").strip().lower()
        if ment == "i":
            ujnev = input("Új mátrix neve: ").strip().upper()
            fajl = "matrixok/" + ujnev + ".csv"
            eredmeny.fajlba_ir(fajl)
            print("Mentve.")

        input("\nTovább (enter)...")


def menu4():
    '''Itt először ki kell választanod a mátrixot.
    Aztán az algoritmust. Kiírja az eredményt, az eredményt
    elmentheted új mátrixként.'''
    pyconio.clrscr()
    print("\n------ ALGORITMUSOK ------\n")

    while True:
        nev = input("Add meg a mátrix nevét: ").strip().upper()
        if nev == "..":
            return
        elif nev == "0":
            kilepes()
            exit()

        fajl = nev + ".csv"

        try:
            A = fajlbol_olvas(fajl)
            break
        except FileNotFoundError:
            print("Nincs ilyen mátrix (A).")
            continue

    while True:
        pyconio.clrscr()
        print(f"MÁTRIX A: {nev}\n")
        print(A)
        print('''
-----------------------------
Válassz algoritmust:

1. Determináns
2. Rang
3. Gauss-elimináció
4. Inverz
5. Egyenletrendszer megoldása (Ax = b)

.. Vissza | 0. Kilépés
''')

        valasz = input("Választás: ").strip()

        if valasz == "..":
            return
        elif valasz == "0":
            kilepes()
            exit()

        elif valasz == "1":
            try:
                eredmeny = determinans(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print("DETERMINÁNS:\n")
            print(eredmeny)
            input("\nTovább (enter)...")
            continue

        elif valasz == "2":
            try:
                eredmeny = rang(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print("RANG:\n")
            print(eredmeny)
            input("\nTovább (enter)...")
            continue

        elif valasz == "3":
            try:
                eredmeny = gauss(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print("GAUSS-ELIMINÁCIÓ EREDMÉNY:\n")
            print(eredmeny)

            ment = input("\nMentsem mátrixként? (i/n): ").strip().lower()
            if ment == "i":
                ujnev = input("Új név: ").strip().upper()
                fajl = "matrixok/" + ujnev + ".csv"
                eredmeny.fajlba_ir(fajl)
                print("Mentve.")

            input("\nTovább (enter)...")
            continue

        elif valasz == "4":
            try:
                eredmeny = inverz(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print("INVERZ:\n")
            print(eredmeny)

            ment = input("\nMentsem mátrixként? (i/n): ").strip().lower()
            if ment == "i":
                ujnev = input("Új név: ").strip().upper()
                fajl = "matrixok/" + ujnev + ".csv"
                eredmeny.fajlba_ir(fajl)
                print("Mentve.")

            input("\nTovább (enter)...")
            continue

        elif valasz == "5":
            print("\nEgyenletrendszer – Ax = b")

            while True:
                nevb = input("Add meg a megoldás mátrix nevét: ").strip().upper()
                if nevb == "..":
                    break
                elif nevb == "0":
                    kilepes()
                    exit()

                fajl_b = nevb + ".csv"
                try:
                    b = fajlbol_olvas(fajl_b)
                    break
                except FileNotFoundError:
                    print("Nincs ilyen mátrix (b).")

            if nevb == "..":
                continue

            try:
                eredmeny = egyenletrendszer(A, b)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print("MEGOLDÁS x:\n")
            print(eredmeny)

            ment = input("\nMentsem mátrixként? (i/n): ").strip().lower()
            if ment == "i":
                ujnev = input("Új név: ").strip().upper()
                fajl = "matrixok/" + ujnev + ".csv"
                eredmeny.fajlba_ir(fajl)
                print("Mentve.")

            input("\nTovább (enter)...")
            continue

        else:
            print("Érvénytelen választás.")
            input("Enter...")

    
def kilepes():
    pass

fomenu()