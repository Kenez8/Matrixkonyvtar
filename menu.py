# Kenéz Máté B6ONGN 2025.11.30.

import pyconio
from matrix import *
from algoritmusok import *
from muveletek import *

def keret(szoveg):
    pyconio.textcolor(pyconio.LIGHTGREEN)
    vonal = "╔" + "═" * 78 + "╗\n"
    also = "╚" + "═" * 78 + "╝\n"

    ki = vonal
    for sor in szoveg.split("\n"):
        s = sor[:78]  # truncate safety
        ki += "║" + s.ljust(78) + "║\n"
    ki += also
    return ki

def fomenu():
    while True:
        pyconio.clrscr()

        print(keret(
"""                              MÁTRIX FŐMENÜ

Válassz a menüpontok közül:

1. Új mátrix létrehozása
2. Mátrixok kezelése
3. Műveletek
4. Algoritmusok

0. Kilépés"""
        ))

        try:
            valasz = int(input("Választás: "))
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
            print("Hiba!: Számot adj meg (0–4).")
            continue

def menu1():
    pyconio.clrscr()
    while True:

        print(keret(
"""                           ÚJ MÁTRIX LÉTREHOZÁSA

Válassz az alábbi lehetőségek közül:

1. Egységmátrix létrehozása
2. Mátrix megadása kézzel

.. Vissza
0. Kilépés"""
        ))

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
            print("Hibás választás! (0–2 vagy ..)")

def menu2():
    while True:
        pyconio.clrscr()

        print(keret(
"""                              MÁTRIXOK KEZELÉSE

Add meg a mátrix nevét, amit kezelni szeretnél!

.. Vissza
0. Kilépés"""
        ))

        valasz = input("Választás: ").strip().upper()
        if valasz == "..":
            return
        elif valasz == "0":
            kilepes()
            exit()

        fajlnev = valasz + ".csv"

        try:
            matrix = fajlbol_olvas(fajlnev)
        except FileNotFoundError:
            print(f"Nincs ilyen mátrix: {fajlnev}")
            continue

        # második menü
        while True:
            pyconio.clrscr()

            fejl = f"KIVÁLASZTOTT MÁTRIX: {valasz}\n\n{matrix}\n\n"
            print(keret(
fejl +
"""1. Módosítás
2. Törlés

.. Vissza
0. Kilépés"""
            ))

            muvelet = input("Választás: ").strip()

            if muvelet == "..":
                return
            elif muvelet == "0":
                kilepes()
                exit()

            elif muvelet == "1":
                modosit_matrix(matrix, fajlnev)
                return

            elif muvelet == "2":
                torol_matrix(fajlnev)
                print("Mátrix törölve.")
                return

            else:
                print("Érvénytelen választás.")


def menu3():
    pyconio.clrscr()
    # 1) Első mátrix kiválasztása

    while True:
        print(keret(
"""                                 MŰVELETEK

Add meg a mátrix nevét, amin műveleteket szeretnél végezni.

.. Vissza
0. Kilépés"""
        ))

        nev1 = input("Melyik mátrix? ").strip().upper()
        if nev1 == "..":
            return
        if nev1 == "0":
            kilepes()
            exit()

        fajl1 = nev1 + ".csv"

        try:
            A = fajlbol_olvas(fajl1)
            break
        except FileNotFoundError:
            print("Nincs ilyen mátrix.")
            continue

    # 2) művelet választás
    while True:
        pyconio.clrscr()
        fejlec = f"MÁTRIX: {nev1}\n\n{A}\n\n"

        print(keret(
fejlec +
"""1. Transzponálás
2. Skalárral szorzás
3. Mátrix + Mátrix
4. Mátrix - Mátrix
5. Mátrix * Mátrix

.. Vissza
0. Kilépés"""
        ))

        valasz = input("Választás: ").strip()

        if valasz == "..":
            return
        elif valasz == "0":
            kilepes()
            exit()

        # egymátrixos műveletek
        elif valasz == "1":
            eredmeny = transzponal(A)

        elif valasz == "2":
            try:
                k = float(input("Skalár: "))
            except ValueError:
                print("Nem szám.")
                continue
            eredmeny = skalarral_szoroz(A, k)

        # többmátrixos
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
            else:
                eredmeny = szorzas(A, B)

        else:
            print("Érvénytelen választás.")
            continue

        # eredmény kiírás
        pyconio.clrscr()
        print(keret("EREDMÉNY:\n\n" + str(eredmeny)))

        ment = input("Mentsem? (i/n): ").strip().lower()
        if ment == "i":
            ujnev = input("Új név: ").strip().upper()
            fajl = "matrixok/" + ujnev + ".csv"
            eredmeny.fajlba_ir(fajl)
            print("Mentve.")

        input("Enter a folytatáshoz...")

def menu4():
    pyconio.clrscr()

    # mátrix kiválasztása
    while True:
        print(keret(
"""                                 ALGORITMUSOK

Add meg a mátrix nevét:

.. Vissza
0. Kilépés"""
        ))

        nev = input("Melyik mátrix? ").strip().upper()
        if nev == "..":
            return
        if nev == "0":
            kilepes()
            exit()

        fajl = nev + ".csv"

        try:
            A = fajlbol_olvas(fajl)
            break
        except FileNotFoundError:
            print("Nincs ilyen mátrix.")
            continue

    # algoritmus menü
    while True:
        pyconio.clrscr()
        fejlec = f"MÁTRIX A: {nev}\n\n{A}\n\n"

        print(keret(
fejlec +
"""1. Determináns
2. Rang
3. Gauss-elimináció
4. Inverz
5. Egyenletrendszer – Ax=b

.. Vissza
0. Kilépés"""
        ))

        valasz = input("Választás: ").strip()

        if valasz == "..":
            return
        if valasz == "0":
            kilepes()
            exit()

        # determináns
        if valasz == "1":
            try:
                eredm = determinans(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print(keret("DETERMINÁNS:\n\n" + str(eredm)))
            input("Enter...")
            continue

        # rang
        if valasz == "2":
            try:
                eredm = rang(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print(keret("RANG:\n\n" + str(eredm)))
            input("Enter...")
            continue

        # Gauss
        if valasz == "3":
            try:
                eredm = gauss(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print(keret("GAUSS-ELIMINÁCIÓ:\n\n" + str(eredm)))

            ment = input("Mentsem? (i/n): ").strip().lower()
            if ment == "i":
                uj = input("Új név: ").strip().upper()
                eredm.fajlba_ir("matrixok/" + uj + ".csv")

            input("Enter...")
            continue

        # inverz
        if valasz == "4":
            try:
                eredm = inverz(A)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print(keret("INVERZ:\n\n" + str(eredm)))

            ment = input("Mentsem? (i/n): ").strip().lower()
            if ment == "i":
                uj = input("Új név: ").strip().upper()
                eredm.fajlba_ir("matrixok/" + uj + ".csv")

            input("Enter...")
            continue

        # egyenletrendszer
        if valasz == "5":
            print("Add meg b mátrix nevét (Ax=b):")
            while True:
                nevb = input("> ").strip().upper()
                if nevb == "..":
                    break
                if nevb == "0":
                    kilepes()
                    exit()

                try:
                    b = fajlbol_olvas(nevb + ".csv")
                    break
                except FileNotFoundError:
                    print("Nincs ilyen mátrix.")

            if nevb == "..":
                continue

            try:
                eredm = egyenletrendszer(A, b)
            except Exception as e:
                print(f"Hiba: {e}")
                input("Enter...")
                continue

            pyconio.clrscr()
            print(keret("MEGOLDÁS x:\n\n" + str(eredm)))

            ment = input("Mentsem? (i/n): ").strip().lower()
            if ment == "i":
                uj = input("Új név: ").strip().upper()
                eredm.fajlba_ir("matrixok/" + uj + ".csv")

            input("Enter...")
            continue

        print("Érvénytelen választás.")
        input("Enter...")

def kilepes():
    pass

fomenu()
