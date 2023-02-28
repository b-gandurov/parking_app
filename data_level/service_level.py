from data_level.ParkinglotDatabase import ParkinglotDatabase
from data_level.TimeRangesDatabase import TimeRangesDatabase
from data_level.database_setup import DatabaseCon, conn


# parking_database = ParkinglotDatabase()


class Vehicle:
    """This class will represent each vehicle parked in the parking lot.
    It will have attributes such as the vehicle type, entry time, exit time,
    and the amount owed for parking."""
    ParkingDB = ParkinglotDatabase()
    VEHICLE_TYPES = ParkingDB.get_valid_vehicles()
    DISCOUNTS = ParkingDB.get_valid_discounts()

    TimeDB = TimeRangesDatabase()

    def __init__(self, vehicle_type, plate_number, entry_time, discount_type):
        self.vehicle_type = vehicle_type
        self.plate_number = plate_number
        self.entry_time = entry_time
        self.discount_type = discount_type

    @property
    def vehicle_type(self):
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value):
        if value not in self.VEHICLE_TYPES:
            raise Exception("Invalid entry")
        else:
            self.__vehicle_type = value

    # @property
    # def discount_type(self):
    #     return self.__discount_type
    #
    # @discount_type.setter
    # def discount_type(self, value):
    #     if value in self.DISCOUNTS:
    #         self.__vehicle_type = value
    #     else:
    #         self.__discount_type = None

    def amount_owed(self):
        """This method will calculate the owed amount for the vehicle"""
        pass

    def exit_time(self):
        """This method will update the exit time once the car exits"""
        return self.TimeDB.get_exited_at(self.plate_number)


class ParkingLotService(ParkinglotDatabase):
    """This class will be responsible for managing the parking lot and its associated data.
    It will be responsible for adding and removing vehicles from the parking lot, checking the
    availability of parking spaces."""

    def __init__(self):
        super().__init__()

    def add_vehicle(self, vehicle: Vehicle):
        # if self.available_space(vehicle.vehicle_type):
        details = (vehicle.plate_number, vehicle.entry_time, vehicle.vehicle_type, vehicle.discount_type)
        self.add_to_parking(*details)

    # else:
    #     raise Exception('No available space')

    def remove_vehicle(self, plate_number, exit_time=None):
        # details = (vehicle.plate_number, vehicle.)
        self.remove_from_parking(plate_number, exit_time)

    # def available_space(self, vehicle_type):
    #     check = self.db.available_space() - self.db.get_vehicle_size(vehicle_type)
    #     return check >= 0


class TimeService(TimeRangesDatabase):
    """This class will provide methods for working with dates and times,
    such as calculating the duration of a vehicle's stay in the parking lot."""

    def __init__(self):
        super().__init__()

    def get_vehicle_time(self, license_plate):
        return self.get_vehicle_start_end_time_in_datetime(license_plate)



class DiscountService:
    """This class will be responsible for managing discounts for parking"""


class PaymentService:
    """This class will be responsible for calculating the amount owed for parking."""
    def __init__(self):
        pass

    def get_amount_owed(self,license_plate):
        pass



class ExceptionHandling:
    """The service layer should include appropriate exception handling to handle errors
    and unexpected situations that may arise during the course of the application's operation."""


# car1 = Vehicle("A", "CA1263HA", "2022-03-01 10:30:00", "Silver")
# car2 = Vehicle("B", "CA4121HA", "2022-03-02 10:30:00", "Gold")
# car3 = Vehicle("B", "CA41212HA", "2022-03-02 10:30:00", "Gold")
# car4 = Vehicle("A", "CA4dwa12HA", "2022-05-02 10:30:00", "Gold")
car5 = Vehicle("A", "CA4dwa1wad2HA", "2022-05-02 10:30:00", "Gold")

# ParkingLotService().add_vehicle(car1)
# ParkingLotService().add_vehicle(car2)
# # # ParkingLotService().ParkingDB.cursor.execute(f'''UPDATE parking_lot_size SET available_area = 1 WHERE id = 1''')
# ParkingLotService().add_vehicle(car3)
ParkingLotService().add_vehicle(car5)
# ParkingLotService().remove_vehicle("CA1263HA","2022-03-02 00:30:00")
# ParkingLotService().remove_vehicle("CA4121HA","2022-03-03 23:30:00")


# print(TimeService().get_vehicle_time("CA1263HA"))
