# Makro-Finanzdashboard

Ein reines HTML/CSS/JS-Dashboard mit Chart.js fuer ein kompaktes,
investor-orientiertes Makro-Finanzmonitoring.

## Module

1. Fear and Greed Index US-Aktienmarkt
2. CHF/USD Chart mit taeglicher Veraenderung
3. REPO-Marktdaten mit taeglicher Veraenderung
4. FED-Bilanz mit aktuellem Stand, Updates und Veraenderung
5. Privatkreditschulden und Trend
6. Uran-Spotpreis und Veraenderung
7. Uran-Defizit
8. Kernenergieanteil am globalen Stromverbrauch und Trend
9. Globaler Strommix und Trends
10. Prognosen fuer Uranenergie-Wachstum
11. Rohstoff- und Materialengpaesse / Defizite
12. Strategische Oelreserven wichtiger Laender

## Starten

Direkt im Browser:

```bash
open index.html
```

Oder mit einem lokalen Server:

```bash
python3 -m http.server 8000
```

Dann `http://localhost:8000` im Browser oeffnen.

## Als PWA auf dem iPhone testen

1. Lokalen Server starten: `python3 -m http.server 8000`
2. iPhone und Rechner ins gleiche Netzwerk bringen.
3. Auf dem iPhone die lokale Rechner-IP mit Port oeffnen, zum Beispiel
   `http://192.168.1.23:8000`.
4. In Safari `Teilen` -> `Zum Home-Bildschirm` auswaehlen.

Die App enthaelt `manifest.json`, `service-worker.js`, iOS-PWA-Meta-Tags und
lokale App-Icons.

Das Dashboard nutzt feste Beispielwerte aus der Aufgabenstellung und
Dummy-Zeitreihen fuer Bereiche ohne angebundene Live-Datenquelle.
