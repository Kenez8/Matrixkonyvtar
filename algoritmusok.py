#Kenéz Máté B6ONGN 2025.11.30.

from matrix import Matrix

def masolat(A):
    """Kézi mátrix-másolás (deep copy nélkül, modulfüggetlenül)."""
    uj = []
    for sor in A.adatok:
        uj.append([x for x in sor])
    return Matrix(A.sor, A.oszlop, uj)

def gauss(A):
    """
    Felső háromszögű mátrixot készít.
    Az eredeti mátrixot NEM módosítja, egy másolaton dolgozik.
    A visszatérési érték maga a módosított mátrix (Matrix objektum).
    """
    M = masolat(A)
    n = M.sor
    m = M.oszlop

    for k in range(min(n, m)):
        if M.adatok[k][k] == 0:
            csere = -1
            for i in range(k+1, n):
                if M.adatok[i][k] != 0:
                    csere = i
                    break
            if csere == -1:
                continue
            M.adatok[k], M.adatok[csere] = M.adatok[csere], M.adatok[k]

        pivot = M.adatok[k][k]

        if pivot == 0:
            continue

        for i in range(k+1, n):
            faktor = M.adatok[i][k] / pivot
            for j in range(k, m):
                M.adatok[i][j] -= faktor * M.adatok[k][j]

    return M

def determinans(A):
    """Determináns kiszámítása Gauss-eliminációval."""
    if A.sor != A.oszlop:
        raise ValueError("A determinánshoz négyzetes mátrix kell.")

    M = masolat(A)
    n = M.sor
    det = 1.0

    # Gauss, de számoljuk a cseréket is a (-1)^cserék miatt
    cserek = 0

    for k in range(n):
        if M.adatok[k][k] == 0:
            csere = -1
            for i in range(k+1, n):
                if M.adatok[i][k] != 0:
                    csere = i
                    break

            if csere == -1:
                return 0.0

            M.adatok[k], M.adatok[csere] = M.adatok[csere], M.adatok[k]
            cserek += 1

        pivot = M.adatok[k][k]
        det *= pivot

        for i in range(k+1, n):
            faktor = M.adatok[i][k] / pivot
            for j in range(k, n):
                M.adatok[i][j] -= faktor * M.adatok[k][j]

    if cserek % 2 == 1:
        det = -det

    return det

def rang(A):
    """Rang = nem nullás sorok száma a Gauss után."""
    M = gauss(A)
    r = 0

    for sor in M.adatok:
        van_nemnulla = any(abs(x) > 1e-9 for x in sor)
        if van_nemnulla:
            r += 1

    return r

def inverz(A):
    """Mátrix inverze Gauss–Jordan módszerrel."""
    if A.sor != A.oszlop:
        raise ValueError("Inverz csak négyzetes mátrixhoz létezik.")

    n = A.sor

    M = [row[:] for row in A.adatok]
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    for k in range(n):
        if M[k][k] == 0:
            csere = -1
            for i in range(k+1, n):
                if M[i][k] != 0:
                    csere = i
                    break
            if csere == -1:
                raise ValueError("A mátrix szinguláris. Nincs inverz.")

            M[k], M[csere] = M[csere], M[k]
            I[k], I[csere] = I[csere], I[k]

        pivot = M[k][k]
        if pivot == 0:
            raise ValueError("A mátrix szinguláris. Nincs inverz.")

        # normálás
        for j in range(n):
            M[k][j] /= pivot
            I[k][j] /= pivot

        # nullázás minden más sorban
        for i in range(n):
            if i == k:
                continue
            faktor = M[i][k]
            for j in range(n):
                M[i][j] -= faktor * M[k][j]
                I[i][j] -= faktor * I[k][j]

    return Matrix(n, n, I)

def egyenletrendszer(A, b):
    """
    Ax = b megoldása Gauss-elimináció + visszahelyettesítés.
    b 1 oszlopú mátrix.
    """
    if A.sor != b.sor:
        raise ValueError("A sorainak és b sorainak egyeznie kell.")

    if b.oszlop != 1:
        raise ValueError("A megoldás mátrix csak 1 dimenziós oszlopvektor lehet.")

    n = A.sor
    M = [sor[:] for sor in A.adatok]
    B = [s[0] for s in b.adatok]

    for k in range(n):
        if M[k][k] == 0:
            csere = -1
            for i in range(k+1, n):
                if M[i][k] != 0:
                    csere = i
                    break
            if csere == -1:
                raise ValueError("A rendszer nem megoldható (nincs pivot).")

            M[k], M[csere] = M[csere], M[k]
            B[k], B[csere] = B[csere], B[k]

        pivot = M[k][k]

        for i in range(k+1, n):
            faktor = M[i][k] / pivot
            for j in range(k, n):
                M[i][j] -= faktor * M[k][j]
            B[i] -= faktor * B[k]

    x = [0] * n
    for i in reversed(range(n)):
        osszeg = B[i]
        for j in range(i+1, n):
            osszeg -= M[i][j] * x[j]

        if M[i][i] == 0:
            raise ValueError("A rendszer nem egyértelműen megoldható.")

        x[i] = osszeg / M[i][i]

    x_adatok = [[xi] for xi in x]
    return Matrix(n, 1, x_adatok)