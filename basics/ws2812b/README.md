# WS2812b
5V-RGB-LED mit einer einzigen Datenleitung.

## Elektrische Spezifikationen
  * Stromverbrauch
  * Spannungsabfall pro Streifen
  * Anzahl PWM-Stufen, (und Art: linear oder anders?)

## Protokoll


## Online Resourcen

# VSCode
Öffnen Sie den Ordner ws2812b mit Visual Code (z.B. mit File->Open Folder). Stimmen Sie der Installation von PlatformIO zu. Es werden alle benötigten Pakete heruntergeladen. Wenn das erledigt ist, kann die Datei src/main.cpp auf den ESP32 übertragen werden (bzw. das kompilierte Programm).

Wenn unter Linux ein Problem mit `/dev/ttyUSB0` auftritt, muss der Benutzer noch der Gruppe `dialout` hinzugefügt werden.
