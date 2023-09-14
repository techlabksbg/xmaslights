import numpy as np


# Eine Datei mit den Daten wird auf der Kommandozeile erwartet.
#
# Die Datei enthält:
#   3 Zahlen durch Leerschläge getrennt -> Position der Kamera
#   1 Zahl -> Höhe der höchsten LED (Annahme auf z-Achse)
#   restliche Zeilen:
#     3 Zahlen druch Leerschläge getrennt: (p,q)-Koordinaten und Messqualität




# Vektoren erstellen:
# a,b,s1 in (p,q)-Koordinaten

# Daraus Matrix A erstellen

# Matrix B erstellen

# Transformationsmatrix T erstellen
# T = B * A^-1

# Matrix C mit allen (p,q,1)-Vektoren erstellen

# P = T*C ergibt alle Punkte P in der Projektionsebene.

# Ausgabe-Dateinamen erstellen (aus eingabe.txt mach eingabe-lines.txt)
# Datei schreiben mit
# Kameraposition (3 Zahlen, durch Leerschläge getrennt)
# Alle Punkte P plus Messqualität, 
#     einer pro Zeile, die vier Zahlen durch Leerschläge getrennt.

