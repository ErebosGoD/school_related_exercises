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

        # Linie zwischen den Wegpunkten zeichnen
        polyline = folium.PolyLine(
            locations=waypoints,
            color='blue',  # Farbe der Linie
            weight=3,       # Dicke der Linie
        ).add_to(m)

        # Wegpunkte zur Karte hinzufügen
        for waypoint in waypoints:
            folium.Marker(
                location=[waypoint[0], waypoint[1]],
                icon=None  # Sie können ein benutzerdefiniertes Icon hinzufügen
            ).add_to(m)

        # Karte in HTML speichern
        m.save(r'gpxdataprocessing\templates\track_map.html')
    else:
        return "Keine Daten für den ausgewählten Track gefunden."

    # Verbindung zur Datenbank schließen
    conn.close()


display_first_track_on_map('AA')
