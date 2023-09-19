from flask import Flask, render_template, redirect, url_for
from flask_caching import Cache
import sqlite3
import folium

app = Flask(__name__)

# Flask-Caching-Konfiguration
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Konfigurieren Sie Ihre SQLite-Datenbankverbindung hier
DATABASE = 'gpxdataprocessing\gpxdata.db'


@app.route('/')
def list_initials():
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Initialen aus der Datenbank abrufen
    cursor.execute('SELECT DISTINCT initials FROM drivers')
    initials_list = [row[0] for row in cursor.fetchall()]

    # Verbindung zur Datenbank schließen
    conn.close()

    return render_template('initials_list.html', initials_list=initials_list)


@app.route('/tracks/<initials>')
@cache.cached(timeout=3600)
def list_tracks(initials):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Tracks für die ausgewählten Initialen abrufen
    cursor.execute('''
        SELECT track_id FROM tracks
        WHERE driver_id = (
            SELECT driver_id FROM drivers
            WHERE initials = ?
        )
    ''', (initials,))

    track_ids = [row[0] for row in cursor.fetchall()]

    # Verbindung zur Datenbank schließen
    conn.close()

    return render_template('track_list.html', initials=initials, track_ids=track_ids)


@app.route('/track/<int:track_id>')
def display_track(track_id):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Wegpunkte für den ausgewählten Track abrufen
    cursor.execute('''
        SELECT latitude, longitude FROM waypoints
        WHERE track_id = ?
    ''', (track_id,))

    waypoints = cursor.fetchall()

    if waypoints:
        # Karte erstellen
        m = folium.Map(location=[waypoints[0][0],
                       waypoints[0][1]], zoom_start=14)

        folium.PolyLine(
            locations=waypoints,
            color='blue',  # Farbe der Linie
            weight=3,       # Dicke der Linie
        ).add_to(m)

        # Wegpunkte zur Karte hinzufügen
        # for waypoint in waypoints:
        #    folium.Marker(
        #        location=[waypoint[0], waypoint[1]],
        #        icon=None  # Sie können ein benutzerdefiniertes Icon hinzufügen
        #    ).add_to(m)

        # Karte in HTML speichern
        m.save(r'gpxdataprocessing\templates\track_map.html')
    else:
        return "Keine Daten für den ausgewählten Track gefunden."

    # Verbindung zur Datenbank schließen
    conn.close()

    return render_template('track_map.html')


if __name__ == '__main__':
    app.run(debug=True)
