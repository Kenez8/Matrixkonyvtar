#Kenéz Máté B6ONGN 2025.11.30.

from matrix import Matrix

def osszead(A, B):
    """A két mátrixnak a méreteinek megkell egyeznie. Ha ez igaz, akkor az
    "A" mátrix minden elemét összeadjuk a megfelelő "B" mátrix elemével"""
    if A.sor != B.sor or A.oszlop != B.oszlop:
        raise ValueError("A két mátrix mérete nem egyezik meg (összeadás).")

    uj_adatok = []
    for i in range(A.sor):
        sor = []
        for j in range(A.oszlop):
            sor.append(A.adatok[i][j] + B.adatok[i][j])
        uj_adatok.append(sor)

    return Matrix(A.sor, A.oszlop, uj_adatok)

def kivon(A, B):
    """A két mátrixnak a méreteinek megkell egyeznie. Ha ez igaz, akkor az
    "A" mátrix minden eleméből kivonjuk a "B" mátrix megfelelő elemét"""
    if A.sor != B.sor or A.oszlop != B.oszlop:
        raise ValueError("A két mátrix mérete nem egyezik meg (kivonás).")

    uj_adatok = []
    for i in range(A.sor):
        sor = []
        for j in range(A.oszlop):
            sor.append(A.adatok[i][j] - B.adatok[i][j])
        uj_adatok.append(sor)

    return Matrix(A.sor, A.oszlop, uj_adatok)

def szorzas(A, B):
    """A szorzáshoz A oszlopszáma meg kell egyezzen B sorszámával. Ha ez igaz, akkor
    """
    if A.oszlop != B.sor:
        raise ValueError("A szorzáshoz A oszlopszáma meg kell egyezzen B sorszámával.")

    eredmeny = []
    for i in range(A.sor):
        sor = []
        for j in range(B.oszlop):
            osszeg = 0
            for k in range(A.oszlop):
                osszeg += A.adatok[i][k] * B.adatok[k][j]
            sor.append(osszeg)
        eredmeny.append(sor)

    return Matrix(A.sor, B.oszlop, eredmeny)

def transzponal(A):
    uj_adatok = []

    for j in range(A.oszlop):
        sor = []
        for i in range(A.sor):
            sor.append(A.adatok[i][j])
        uj_adatok.append(sor)

    return Matrix(A.oszlop, A.sor, uj_adatok)

def skalarral_szoroz(A, k):
    uj_adatok = []

    for i in range(A.sor):
        sor = []
        for j in range(A.oszlop):
            sor.append(A.adatok[i][j] * k)
        uj_adatok.append(sor)

    return Matrix(A.sor, A.oszlop, uj_adatok)
