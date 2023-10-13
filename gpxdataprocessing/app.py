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
    # set default location and zoom
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

    map_html = m.get_root()._repr_html_()
    return render_template('onepager.html', map_html=map_html)


@app.route('/get_initials', methods=['GET'])
def get_initials():
    # create connection to sqlite3 database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # get initials from database
    cursor.execute('SELECT DISTINCT initials FROM drivers')
    initials = [row[0] for row in cursor.fetchall()]

    # close database
    conn.close()

    # return initials as json
    return jsonify(initials)


@app.route('/get_tracks/<initials>', methods=['GET'])
def get_tracks(initials):
    # create connection to sqlite3 database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # get tracks for chosen initials
    cursor.execute('''
        SELECT tracks.track_id
        FROM tracks
        INNER JOIN drivers ON tracks.driver_id = drivers.driver_id
        WHERE drivers.initials = ?
    ''', (initials,))

    track_ids = [row[0] for row in cursor.fetchall()]

    conn.close()

    # return track ids as json
    return jsonify(track_ids)


@app.route('/display_track/<int:track_id>', methods=['GET'])
def display_track(track_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # get latitude and longitude for given track id
    cursor.execute('''
        SELECT latitude, longitude
        FROM waypoints
        WHERE track_id = ?
    ''', (track_id,))

    waypoints = cursor.fetchall()

    # create map with default location germany
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

    if waypoints:
        folium.PolyLine(
            locations=waypoints,
            color='blue',
            weight=3,
        ).add_to(m)

        # calculate map borders
        latitudes = [wp[0] for wp in waypoints]
        longitudes = [wp[1] for wp in waypoints]
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)
        bounds = [[min_lat, min_lon], [max_lat, max_lon]]

        # fit map to bounds of container
        m.fit_bounds(bounds)

    # return map
    map_html = m.get_root()._repr_html_()
    return map_html


if __name__ == '__main__':
    gpx_parser = GpxParser(DATABASE)
    # gpx_parser.create_tables()
    # gpx_parser.persist_gpx_data(GPX_DIRECTORY)
    app.run()
