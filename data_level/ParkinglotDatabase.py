from datetime import datetime

from data_level.database_setup import DatabaseCon


class ParkinglotDatabase(DatabaseCon):

    def __init__(self):
        super().__init__()
        # self.available_space = self.get_parking_lot_size()

    # def get_parking_lot_size(self):
    #
    #
    # @property
    # def available_space(self):
    #     return self.__available_space
    #
    def available_space(self):
        result = self.cursor.execute("SELECT available_area FROM parking_lot_size").fetchone()[0]
        if result is not None:
            return result
        else:
            raise Exception("Unable to retrieve parking lot size from database")

    @staticmethod
    def get_as_list(iterable):
        return [row[0] for row in iterable]

    def get_valid_vehicles(self):
        return self.get_as_list(self.cursor.execute("SELECT type FROM vehicles_types").fetchall())

    def get_valid_discounts(self):
        return self.get_as_list(self.cursor.execute("SELECT type, rate FROM discount").fetchall())

    # def __search_function(self, select_table_column, table, where_type_of_data, searched_item):
    #     result = self.cursor.execute(
    #         f"SELECT {select_table_column} FROM {table} WHERE {where_type_of_data} = ?", (searched_item,)).fetchval()
    #     if result is None:
    #         return None
    #     return result

    # checks to be made for add parking
    # # check 1 - if the vehicle type is valid
    # vehicle_type_check = self.__search_function("id", "vehicles_types", "type", vehicle_type)
    # if vehicle_type_check is None:
    #     raise Exception("Invalid data type for vehicle type")
    # # check 2
    # discount_plan = self.__search_function("type", "discount", "type", discount)

    def get_vehicle_size(self, value):
        # value is either vehicle type or license plate
        if len(value) == 1:
            return self.cursor.execute(f'''SELECT area FROM vehicles_types WHERE type = ? ''', value).fetchone()[0]
        result = \
            self.cursor.execute(f'''SELECT type_vehicle FROM vehicles WHERE plate_number = ? ''', (value,)).fetchone()[0]
        return self.cursor.execute(f'''SELECT area FROM vehicles_types WHERE type = ?''', result).fetchone()[0]

    def add_to_parking(self, license_plate, entry_time, vehicle_type, discount):
        self.cursor.execute(
            "INSERT INTO vehicles (plate_number,entered_at,type_vehicle,discount) "
            "VALUES (?,?,?,?)",
            (license_plate, entry_time, vehicle_type, discount))
        parking_spot = self.get_vehicle_size(vehicle_type)
        diff = self.available_space() - parking_spot
        if diff >= 0:
            self.cursor.execute(f'''UPDATE parking_lot_size SET available_area = {diff} WHERE id = 1''')
            self.db.commit()
        else:
            raise Exception("Not enough space in the parkinglot")
        return self.cursor.rowcount >= 1

    # def get_free_space(self):
    #     result = self.cursor.execute('SELECT area - (select SUM) FROM parking_lot_size where id = 1')

    def remove_from_parking(self, license_plate, exit_time):
        if exit_time is None:
            exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(
            "UPDATE vehicles SET exited_at = ? "
            "WHERE plate_number = ? AND exited_at IS NULL",
            (exit_time, license_plate))
        parking_spot = self.get_vehicle_size(license_plate)
        diff = self.available_space() + parking_spot
        default = self.cursor.execute("SELECT starting_area FROM parking_lot_size").fetchone()[0]
        if diff <= default:
            self.cursor.execute(f'''UPDATE parking_lot_size SET available_area = {diff} WHERE id = 1''')
            self.db.commit()
        else:
            raise Exception("Available area cannot exceed default parkinglot size")
        return self.cursor.rowcount >= 1
