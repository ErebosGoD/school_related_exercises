import os
import sqlite3
import gpxpy


def create_connection(database_path):

    # SQLite-Datenbankverbindung herstellen
    conn = sqlite3.connect(database_path)
    return conn


def create_tables(cursor):
    # Tabellen erstellen (falls noch nicht vorhanden)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            initials TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            car_id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tracks (
        track_id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id INTEGER,
        car_id INTEGER,
        FOREIGN KEY (driver_id) REFERENCES drivers (driver_id),
        FOREIGN KEY (car_id) REFERENCES cars (car_id)
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS waypoints (
        waypoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER,
        latitude REAL,
        longitude REAL,
        timestamp TEXT,
        FOREIGN KEY (track_id) REFERENCES tracks (track_id)
        )
    ''')


def persist_gpx_data(cursor):
    # iterate over gpx files in given directory
    for filename in os.listdir(gpx_directory):
        if filename.endswith('.gpx'):
            gpx_file_path = os.path.join(gpx_directory, filename)

            # parse gpx file
            gpx_file = open(gpx_file_path, 'r')
            gpx = gpxpy.parse(gpx_file)

            # extract initials and license plate from file name
            initials = filename[:2]
            license_plate = filename[3:12]
            if license_plate[-1] == '_':
                license_plate = license_plate[:-1]

            # Check if driver already exists
            cursor.execute(
                'SELECT driver_id FROM drivers WHERE initials = ?', (initials,))
            existing_driver = cursor.fetchone()

            if existing_driver:
                # if true use existing driver ID
                driver_id = existing_driver[0]
            else:
                # if falls insert as new driver with new ID
                cursor.execute('INSERT INTO drivers (initials) VALUES (?)',
                               (initials,))
                driver_id = cursor.lastrowid

            # insert license plates
            cursor.execute('INSERT INTO cars (license_plate) VALUES (?)',
                           (license_plate,))

            # insert tracks
            cursor.execute('INSERT INTO tracks (driver_id, car_id) VALUES ((SELECT driver_id FROM drivers WHERE initials = ?), (SELECT car_id FROM cars WHERE license_plate = ?))',
                           (initials, license_plate))

            track_id = cursor.lastrowid

            # insert waypoints
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        cursor.execute('INSERT INTO waypoints (track_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)',
                                       (track_id, point.latitude, point.longitude, str(point.time)))


if __name__ == '__main__':
    # path to database
    database_path = 'gpxdataprocessing\gpxdata.db'

    # directory with gpx files
    gpx_directory = 'gpxdataprocessing\gpx-Dateien'

    conn = create_connection(database_path)

    cursor = conn.cursor()

    create_tables(cursor)

    persist_gpx_data(cursor)

    # commit changes to db
    conn.commit()

    # close connection
    conn.close()
