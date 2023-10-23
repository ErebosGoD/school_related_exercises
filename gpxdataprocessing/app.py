import folium
from flask import Flask, render_template, jsonify
from gpxparser import GpxParser


app = Flask(__name__, static_url_path='/static')

DATABASE = r'gpxdataprocessing\gpxdata.db'
GPX_DIRECTORY = r'gpxdataprocessing\gpxdata'


@app.route('/', methods=['GET'])
def onepager():
    # create database tables if they don't exist
    gpx_parser.create_tables()
    # parse and persist each file in given directory
    gpx_parser.persist_gpx_data(GPX_DIRECTORY)
    # set default location and zoom
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)
    # using private method _repr_html_ instead of render_html since the latter overwrites the css of the html body
    map_html = m.get_root()._repr_html_()
    return render_template('onepager.html', map_html=map_html)


@app.route('/get_initials', methods=['GET'])
def get_initials():
    return jsonify(gpx_parser.get_initials())

# old routes for display each track for the selected initials

# @app.route('/get_tracks/<initials>', methods=['GET'])
# def get_tracks(initials):
#     # create connection to sqlite3 database
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     # get tracks for chosen initials
#     cursor.execute('''
#         SELECT tracks.track_id
#         FROM tracks
#         INNER JOIN drivers ON tracks.driver_id = drivers.driver_id
#         WHERE drivers.initials = ?
#     ''', (initials,))

#     track_ids = [row[0] for row in cursor.fetchall()]

#     conn.close()

#     # return track ids as json
#     return jsonify(track_ids)


# @app.route('/display_track/<int:track_id>', methods=['GET'])
# def display_track(track_id):
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     # get latitude and longitude for given track id
#     cursor.execute('''
#         SELECT latitude, longitude
#         FROM waypoints
#         WHERE track_id = ?
#     ''', (track_id,))

#     waypoints = cursor.fetchall()

#     # create map with default location germany
#     m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

#     if waypoints:
#         folium.PolyLine(
#             locations=waypoints,
#             color='blue',
#             weight=3,
#         ).add_to(m)

#         # calculate map borders
#         latitudes = [wp[0] for wp in waypoints]
#         longitudes = [wp[1] for wp in waypoints]
#         min_lat, max_lat = min(latitudes), max(latitudes)
#         min_lon, max_lon = min(longitudes), max(longitudes)
#         bounds = [[min_lat, min_lon], [max_lat, max_lon]]

#         # fit map to bounds of container
#         m.fit_bounds(bounds)

#     # return map
#     map_html = m.get_root()._repr_html_()
#     return map_html

# display tracks based on initials, car, start date and end date
@app.route('/display_track/<initials>/<car>/<start_date>/<end_date>', methods=['GET'])
def display_filtered_track(initials, car, start_date, end_date):
    # get waypoints for given variables
    waypoints = gpx_parser.get_waypoints_for_track(
        initials, car, start_date, end_date)

    # create map with default location germany
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

    if waypoints:
        # Create a PolyLine to connect the waypoints
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

    # using private method _repr_html_ instead of render_html since the latter overwrites the css of the html body
    map_html = m.get_root()._repr_html_()
    return map_html

# get cars that the driver with the given initials has driven


@app.route('/get_cars/<initials>', methods=['GET'])
def get_cars(initials):
    return jsonify(gpx_parser.get_cars(initials))

# route for resetting the map back to its default position


@app.route('/reset_map', methods=['GET'])
def reset_map():
    default_map = folium.Map(location=[51.1657, 10.4515], zoom_start=6)
    map_html = default_map.get_root()._repr_html_()
    return map_html


if __name__ == '__main__':
    gpx_parser = GpxParser(DATABASE)
    app.run()
