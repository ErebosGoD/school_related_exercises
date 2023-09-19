import folium
import sqlite3


def display_first_track_on_map(driver_initials):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('gpxdataprocessing\gpxdata.db')
    cursor = conn.cursor()

    # Abfrage, um den ersten Track für den angegebenen Fahrer abzurufen
    cursor.execute('''
        SELECT latitude, longitude FROM waypoints
        WHERE track_id = (
            SELECT MIN(track_id) FROM tracks
            WHERE driver_id = (
                SELECT driver_id FROM drivers
                WHERE initials = ?
            )
        )
    ''', (driver_initials,))

    waypoints = cursor.fetchall()

    if waypoints:
        # Karte erstellen
        m = folium.Map(location=[waypoints[0][0],
                       waypoints[0][1]], zoom_start=14)

        # Wegpunkte zur Karte hinzufügen
        for waypoint in waypoints:
            folium.Marker(
                location=[waypoint[0], waypoint[1]],
                icon=None  # Sie können ein benutzerdefiniertes Icon hinzufügen
            ).add_to(m)

        # Karte anzeigen
        m.save(r'gpxdataprocessing\templates\track_map.html')
    else:
        print("Keine Daten für den angegebenen Fahrer gefunden oder der Fahrer hat keinen Track.")

    # Verbindung zur Datenbank schließen
    conn.close()


# Beispielaufruf
display_first_track_on_map('AA')
