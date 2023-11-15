# Übersicht
Der Server läuft auf einem Computer, typischerweise ein Webserver (Apache).
Er kann aber auch lokal betrieben werden und mit dem networked-simulator.py 
benutzt werden.

Der Server empfängt Daten auf Port 15878, UDP vom ESP32, auf TCP (gleiche Portummer) 
antwortet ein einfacher Webserver der den Query-Teil der URL auswertet.

Der Client lauft auf dem ESP32. Die Verbindung ist via UDP auf den Server 15878.

## Protokoll
```
ESP32                   Server

      ---- start ---->
      <--- [254]pong ------

         ca. 50 fps:
      <--- [0/1/255]LED data --
           . . . 
           . . . 
    
       1x pro Sekunde
      ---- ping ---->
      <--- [254]pong ------
```

### LED data
Das erste Byte eines UDP-Packets vom Server ist 254 für eine
Systemnachricht (z.Z. nur pong).
Die Datenpakete sind nummeriert von 0 bis n-2. Das letzte
Datenpakete hat als erstes Byte 255.


# Lokale Ausführung
Zuerst müssen folgende Dinge installiert sein:
  * python (neuste Version aus dem AppStore)
  * Folgende zwei Python-Libraries mit pip installieren:
```
pip install numpy
pip install pygame
```
## Ausführung

In einem Terminal den Server starten mit:
```
python main.py
```

In einem anderen Terminal den Simulator starten mit:
```
python networked-simulator.py
```

Server-Steuerung z.B. via http://localhost:15878/


Oder legen Sie eine Datei ``myconfig.txt`` an, wo die Parameter definiert werden können, die beim Start vom Server gelten sollen:
```text
# Das ist ein Kommentar und wird ignoriert.
# Es folgen Zeilen mit Schlüssel, Abstand, Wert
prg Kugeln
brightness 1.0
saturation 1.0
period 5
```


# Eigene Animation für den Baum
Alle Animation liegen im Verzeichnis ``animations_available``. 

Kopieren Sie z.B. die Datei ``rainbow3d.py`` in eine
neue Datei, z.B. ``superanim.py`` und bennen Sie dort
die Klasse in ``SuperAnim`` um. //Achtung: Im Moment
dürfen in dieser Klasse keine weiteren Klassen definiert sein.//

Damit die Animation auch geladen wird, muss diese im Verzeichnis
``animations_enabled`` verlinkt sein. Folgender Befehl erledigt das:
```bash
cd animations_enabled
ln -si ../animations_available/superanim.py
```
Passen Sie auch die Methode ``defaults`` an. Der Eintrag ``autoplay``
gibt an, für wie viele Sekunden die Animation jeweils automatisch
angezeigt werden soll.

## Hinweise zur Programmierung eigener Animationen
### Parameter
Verwenden Sie die bereits definierten Parameter, bevor Sie neue hinzufügen (siehe auch in der Methode initConfig in der Datei ``main.py``):
  * ``self.config['brightness']``
  * ``self.config['saturation']``
  * ``self.config['period']``
  * ``self.config['color']``
### LEDs
Verwenden Sie die Methoden
  * ``leds.setColor(l, [r,g,b])``  wobei l die Nummer der LED (von 0 bis leds.n-1) ist, und r,g,b die Farbwerte als Ganzzahlen von 0-255.
  * ``c = leds.getColor(l)``  wobei l die Nummer der LED (von 0 bis leds.n-1) ist. Geliefert wird ein Array ``[r,g,b]``.

### Koordinaten der LEDs
``points`` ist ein numpy-Array (Matrix) mit 3 Zeilen und so vielen Spalten wie LEDs (z.Z. 3x800).
Verwendet werden kann points wie folgt:
  * ``p = points[:,l]``  liefert ein numpy-Array mit 3 Einträgen, den Koordinaten der LED mit Nummer l (von 0 bis und mit ``leds.n-1``)

### Praktische numpy Operationen
  * ``np.linalg.norm(v)`` Norm eines Vektors v
  * ``a-b`` Differenz zweier Vektoren
  * ``np.matmul(a,b)`` Produkt der Matrizen a mit b, z.B. wenn ``n`` ein Vektor mit 3 Komponenten ist, liefert ``np.matmul(n, points)`` ein Array der Länge ``leds.n`` mit allen Skalarprodukten von ``n`` mit den Ortvektoren der LED-Positionen.
  * ``math.cos`` und ``math.sin`` etc. arbeiten im Bogenmass und erfordern ein ``import math`` am Anfang der Datei.
