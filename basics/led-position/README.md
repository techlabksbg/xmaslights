# Positionsbestimmung
## Nötige Daten
### Position und Messqualität
Wir gehen davon aus, dass wir für jede LED folgende Daten haben:

    0000 354 217 0.9

Nummer der LED, x- und y-Koordinaten des Pixels auf der Video-Aufnahme und eine Zahl zwischen 0.0 (völlig unzuverlässige Koordinaten) bis 1.0 (sichere und präzise Koordinaten).


### Weitere Daten zur Messung

TODO

## Annahmen zur Kamera
  * Wir nehmen an, dass die Kamera 
«[rectilinear](https://en.wikipedia.org/wiki/Rectilinear_lens)» ist, was eher nicht so ist. Der Fehler sollte aber nicht zu gross sein (könnte man mit einer karrierten Wandtafel gut ausmessen).
  * Wir nehmen an, die Projektionsebene ist normal zur Kameraachse, was bei fast allen Kameras in bester Näherung auch so ist.

### Projektionsebene

![Projektionsebene](https://upload.wikimedia.org/wikipedia/en/thumb/d/d2/Perspectiva-2.svg/578px-Perspectiva-2.svg.png) (Bild Wikimedia)

## Umrechnungen
Wenn immer möglich, werden wir Umrechnungen matriziell formulieren, damit können die Matrix-Funktionen von numpy verwendet werden. Damit können einfach Matrizen invertiert oder ganze Listen von Vektoren transformiert werden.
### Pixel-Position zu räumliche Koordinaten in der Projektionsebene

TODO

$$\vec v = \begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1 \\
\end{pmatrix} \vec v$$

#### Räumliche Position

TODO

