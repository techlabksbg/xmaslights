# Server

Der Server wird im Tech-Lab laufen und besteht aus mehreren Komponenten:
  * Web-Interface (php, html, javascript) für die User-Interaktion (apache2)
  * Steuerungsserver für die Kommunikation zwischen Server (python) und dem ESP32 (C++)

## ESP32 <-> Steuerungsserver
Verbindung via UDP reicht (wenn ein Frame mal nicht durchkommt, ist es eh zu spät).

## Webserver -> Steuerungsserver
Via HTTP-Get Requests (könnten auch direkt weitergeleitet werden)


