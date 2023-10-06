from flask import Flask, render_template, jsonify, url_for
import sqlite3
import folium
from parse_and_persist_data import GpxParser

app = Flask(__name__, static_url_path='/static')

DATABASE = 'gpxdataprocessing\gpxdata.db'
GPX_DIRECTORY = 'gpxdataprocessing\gpxdata'


@app.route('/', methods=['GET'])
def onepager():
    gpx_parser.create_tables()
    gpx_parser.persist_gpx_data(GPX_DIRECTORY)
    # Karte mit einem Standardstandort und Zoom erstellen
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

    # Karte in HTML speichern und in die Vorlage einfügen
    map_html = m.get_root()._repr_html_()
    return render_template('onepager.html', map_html=map_html)


@app.route('/get_initials', methods=['GET'])
def get_initials():
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Abrufen der Initialen aus der Datenbank
    cursor.execute('SELECT DISTINCT initials FROM drivers')
    initials = [row[0] for row in cursor.fetchall()]

    # Verbindung zur Datenbank schließen
    conn.close()

    # Konvertieren Sie die Initialen in JSON und senden Sie sie zurück
    return jsonify(initials)

# Neue Route zum Abrufen der Tracks basierend auf den ausgewählten Initialen als JSON


@app.route('/get_tracks/<initials>', methods=['GET'])
def get_tracks(initials):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Tracks für die ausgewählten Initialen abrufen
    cursor.execute('''
        SELECT tracks.track_id
        FROM tracks
        INNER JOIN drivers ON tracks.driver_id = drivers.driver_id
        WHERE drivers.initials = ?
    ''', (initials,))

    track_ids = [row[0] for row in cursor.fetchall()]

    # Verbindung zur Datenbank schließen
    conn.close()

    # Konvertieren Sie die Track-IDs in JSON und senden Sie sie zurück
    return jsonify(track_ids)

# Neue Route zum Anzeigen eines Tracks basierend auf der ausgewählten Track-ID


@app.route('/display_track/<int:track_id>', methods=['GET'])
def display_track(track_id):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Wegpunkte für den ausgewählten Track abrufen
    cursor.execute('''
        SELECT latitude, longitude
        FROM waypoints
        WHERE track_id = ?
    ''', (track_id,))

    waypoints = cursor.fetchall()

    # Karte erstellen
    # Leere Karte mit Mittelpunkt Deutschland
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

    if waypoints:
        folium.PolyLine(
            locations=waypoints,
            color='blue',
            weight=3,
        ).add_to(m)

        # Berechnen Sie die Grenzen der Karte basierend auf den Wegpunkten
        latitudes = [wp[0] for wp in waypoints]
        longitudes = [wp[1] for wp in waypoints]
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)
        bounds = [[min_lat, min_lon], [max_lat, max_lon]]

        # Verwenden Sie die Grenzen, um die Karte anzupassen
        m.fit_bounds(bounds)

    # Karte in HTML speichern und zurückgeben
    map_html = m.get_root()._repr_html_()
    return map_html


if __name__ == '__main__':
    gpx_parser = GpxParser(DATABASE)
    # gpx_parser.create_tables()
    # gpx_parser.persist_gpx_data(GPX_DIRECTORY)
    app.run()
