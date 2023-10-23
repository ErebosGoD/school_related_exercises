import os
import sqlite3
import gpxpy


class GpxParser():
    def __init__(self, database_path) -> None:
        # create connection and cursor
        self.connection = sqlite3.connect(
            database_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    # create tables if they don't exist
    def create_tables(self):
        # table for files to keep track which files have been parsed already to reduce load times
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT
            )
        ''')
        # table for drivers
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drivers (
                driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                initials TEXT
            )
        ''')
        # table for cars
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_plate TEXT
            )
        ''')
        # table for tracks
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER,
            car_id INTEGER,
            FOREIGN KEY (driver_id) REFERENCES drivers (driver_id),
            FOREIGN KEY (car_id) REFERENCES cars (car_id)
            )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS waypoints (
            waypoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER,
            latitude REAL,
            longitude REAL,
            timestamp TEXT,
            FOREIGN KEY (track_id) REFERENCES tracks (track_id)
            )
        ''')

    def persist_gpx_data(self, gpx_directory):
        # iterate over gpx files in given directory
        for filename in os.listdir(gpx_directory):
            if filename.endswith('.gpx'):
                # Check if file was already parsed
                self.cursor.execute(
                    'SELECT filename FROM files WHERE filename = ?', (filename,))
                current_file = self.cursor.fetchone()

                # if file has not been parsed
                if not current_file:
                    # insert filename into file table
                    self.cursor.execute(
                        'INSERT INTO files (filename) VALUES (?)', (filename,))

                    # create file_path
                    gpx_file_path = os.path.join(gpx_directory, filename)

                    # parse gpx file
                    gpx_file = open(gpx_file_path, 'r', encoding="utf-8")
                    gpx = gpxpy.parse(gpx_file)

                    # extract initials and license plate from file name
                    initials = filename[:2]
                    license_plate = filename[3:12]
                    if license_plate[-1] == '_':
                        license_plate = license_plate[:-1]

                    # Check if driver already exists
                    self.cursor.execute(
                        'SELECT driver_id FROM drivers WHERE initials = ?', (initials,))
                    existing_driver = self.cursor.fetchone()

                    if existing_driver:
                        # if true use existing driver ID
                        driver_id = existing_driver[0]
                    else:
                        # if false, insert as a new driver with a new ID
                        self.cursor.execute(
                            'INSERT INTO drivers (initials) VALUES (?)', (initials,))
                        driver_id = self.cursor.lastrowid

                    # insert license plates
                    self.cursor.execute(
                        'INSERT INTO cars (license_plate) VALUES (?)', (license_plate,))

                    # insert tracks
                    self.cursor.execute('INSERT INTO tracks (driver_id, car_id) VALUES (?, (SELECT car_id FROM cars WHERE license_plate = ?))',
                                        (driver_id, license_plate))

                    track_id = self.cursor.lastrowid

                    if gpx.tracks:
                        for track in gpx.tracks:
                            if track.segments:
                                # If the track has segments, process them
                                for segment in track.segments:
                                    for point in segment.points:
                                        self.cursor.execute('INSERT INTO waypoints (track_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)',
                                                            (track_id, point.latitude, point.longitude, str(point.time)))
                    else:
                        # If there are no tracks, insert individual waypoints
                        for waypoint in gpx.waypoints:
                            self.cursor.execute('INSERT INTO waypoints (track_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)',
                                                (track_id, waypoint.latitude, waypoint.longitude, str(waypoint.time)))
                    self.connection.commit()

    # get initials
    def get_initials(self):
        self.cursor.execute('SELECT DISTINCT initials FROM drivers')
        initials = [row[0] for row in self.cursor.fetchall()]
        self.connection.commit()
        return initials

    # get cars for given initials
    def get_cars(self, initials):
        self.cursor.execute('''
        SELECT DISTINCT cars.license_plate
        FROM cars
        INNER JOIN tracks ON cars.car_id = tracks.car_id
        INNER JOIN drivers ON tracks.driver_id = drivers.driver_id
        WHERE drivers.initials = ?
        ''', (initials,))

        cars = [row[0] for row in self.cursor.fetchall()]
        return cars

    # get waypoints for track based on given variables
    def get_waypoints_for_track(self, initials, car, start_date, end_date):
        self.cursor.execute('''
        SELECT latitude, longitude
        FROM waypoints
        INNER JOIN tracks ON waypoints.track_id = tracks.track_id
        INNER JOIN drivers ON tracks.driver_id = drivers.driver_id
        INNER JOIN cars ON tracks.car_id = cars.car_id
        WHERE drivers.initials = ? AND cars.license_plate = ? AND timestamp BETWEEN ? AND ?
        ''', (initials, car, start_date, end_date))

        waypoints = self.cursor.fetchall()
        return waypoints
