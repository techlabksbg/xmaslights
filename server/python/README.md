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

Server-Steuerung z.B. via http://localhost:15878/?prg=Rainbow3d&brightness=1.0

(zwei mal Laden, damit ein Effekt eintritt)


## Eigene Animation für den Baum
Kopieren Sie z.B. die Datei rainbow3d.py in eine
neue Datei superanim.py und bennen Sie dort
die Klasse in SuperAnim um.

Tragen Sie dann in der Datei main.py den String
"SuperAnim" im Array "progNames" sein.

Setzen Sie im main.py auch die default-Parameter
auf für Sie geeignete Werte, dann können Sie sich
den Webzugriff sparen, wenn Sie den Server neu
starten.