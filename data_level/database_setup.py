import sqlite3
from abc import ABC

database = "parking_app.db"
conn = sqlite3.connect(database)


class DatabaseCon(ABC):
    DB = conn

    def __init__(self):
        self.db = self.DB
        self.cursor = self.db.cursor()

    def get_item(self, return_from_col, table, column_to_match, item_to_match):
        try:
            result = self.cursor.execute(f'''SELECT {return_from_col} FROM {table} WHERE {column_to_match} = ?''',
                                       (item_to_match,)).fetchone()[0]
        except TypeError:
            raise Exception(f"No result for '{item_to_match}' item in '{column_to_match}' column for '{table}' table.")
        return result



if __name__ == "__main__":
    membership_cards = {"Silver": .1, "Gold": .15, "Platinum": 0.2}
    vehicle_types = {"A": 1, "B": 2, "C": 4}
    rate_types = {"night_hours": ["18:00:00", "08:00:00"], "day_hours": ["08:00:00", "18:00:00"]}
    # rate_types = {"night_hours": ["18:00:00", "08:00:00"], "day_hours": ["08:00:00", "18:00:00"],
    # "mid_hours": ["14:00:00", "22:00:00"]}
    rates = {"night_hours": {"A": 2, "B": 4, "C": 8}, "day_hours": {"A": 3, "B": 6, "C": 12}}
    parkinglot_size = 20

    # try:
    with sqlite3.connect("parking_app.db") as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.commit()
        cursor = connection.cursor()

        create_table_parking_lot_size = '''
            CREATE TABLE IF NOT EXISTS parking_lot_size (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                starting_area INTEGER NOT NULL CHECK (starting_area >= 0),
                available_area INTEGER NOT NULL CHECK (available_area >= 0)
            )
        '''

        create_table_vehicles_types = '''
        CREATE TABLE IF NOT EXISTS vehicles_types(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR(16) UNIQUE,
        area INTEGER
        )
        '''
        create_table_discount = '''
        CREATE TABLE IF NOT EXISTS discount(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR(54) UNIQUE,
        rate FLOAT
        )
        '''

        create_table_vehicles = '''
        CREATE TABLE IF NOT EXISTS vehicles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_vehicle VARCHAR(16),
        plate_number VARCHAR(16),
        entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        exited_at DATETIME NULL,
        discount VARCHAR(52) NULL,
        FOREIGN KEY(discount) REFERENCES discount(id),
        FOREIGN KEY(type_vehicle) REFERENCES vehicles_types(id),
        UNIQUE (plate_number)
        )
        '''

        create_table_rate_types = '''CREATE TABLE rate_types
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          rate_type VARCHAR(128),
                          start_time TIMESTAMP, 
                          end_time TIMESTAMP)'''

        cursor.execute(create_table_parking_lot_size)
        cursor.execute(create_table_vehicles_types)
        cursor.execute(create_table_discount)
        cursor.execute(create_table_vehicles)
        cursor.execute(create_table_rate_types)
        cursor.execute('''INSERT INTO parking_lot_size (starting_area, available_area) VALUES (?,?)''',
                       (parkinglot_size, parkinglot_size))
        for rate_type, rates_dict in rates.items():
            table_name = f"{rate_type}"
            cursor.execute(f'''CREATE TABLE {table_name}
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              vehicle VARCHAR(128), 
                              rate FLOAT)''')
            for vehicle, rate in rates_dict.items():
                cursor.execute(f'''INSERT INTO {table_name} (vehicle, rate) VALUES (?, ?)''', (vehicle, rate))

        for rate_type, time_range in rate_types.items():
            cursor.execute('''INSERT INTO rate_types (rate_type, start_time, end_time) VALUES (?, ?, ?)''',
                           (rate_type, time_range[0], time_range[1]))

        for plan, rate in membership_cards.items():
            cursor.execute('''INSERT INTO discount (type, rate) VALUES (?,?)''', (plan, rate))

        for v_type, area in vehicle_types.items():
            cursor.execute('''INSERT INTO vehicles_types (type, area) VALUES (?,?)''', (v_type, area))

        connection.commit()
    # except sqlite3.Error as e:
    #     print(f'The following error has occurred: {str(e)}')
