# xmaslights
EF Informatik: Interaktive RGB-LED Christbaumbeleuchtung in 3D

## Basics
  * [Benötigte Software](basics/software.md)
  * [Minimale «Hello world»-Beispiele](basics/README.md)


## Client-Server Architektur
ESP32 kontaktiert ofi.tech-lab.ch auf Port 15878 via udp. 
Als Antwort werden die LED-Daten binär im RGB-Format (3 Bytes pro LED) 
ebenfalls per UDP gesendet.

Der UDP-Server ist in Python programmiert.

Im gleichen Pythonprogramm wird auch ein http-Server (via TCP Port 15878)
gestartet, worüber mit GET-Requests Parameter gesetzt werden können, mit
denen dann die Programme für die LEDs gesteuert und gewählt werden können.

Dieser Server ist aber nicht direkt erreichbar, sondern es wird im 
Apache2 Webserver ein ReverseProxy eingerichtet.

### OFI-Webserver
Unser account ist `ef05a`. Fügen Sie folgende Zeilen Ihrer lokalen Datei 
`~/.ssh/config` hinzu (bzw. legen Sie die Datei neu an):
```
Host ef
        HostName tech-lab.ch
        User ef05a
        Port 23
```

Kopieren Sie dann Ihren öffentlichen SSH-Schlüssel wie folgt auf den Server:
```
ssh-copy-id ef
```
Das Passwort kriegen Sie von mir und wird danach zurückgesetzt (so dass man sich 
nur noch mit dem SSH-Schlüssel einloggen kann).
 
