from data_level.ParkinglotDatabase import ParkinglotDatabase
from data_level.PaymentDatabase import PaymentDatabase
from data_level.TimeRangesDatabase import TimeRangesDatabase


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


class ParkingLotService(ParkinglotDatabase):
    """This class will be responsible for managing the parking lot and its associated data.
    It will be responsible for adding and removing vehicles from the parking lot, checking the
    availability of parking spaces."""

    def __init__(self):
        super().__init__()

    def add_vehicle(self, vehicle: Vehicle):
        details = (vehicle.plate_number, vehicle.entry_time, vehicle.vehicle_type, vehicle.discount_type)
        self.add_to_parking(*details)

    def remove_vehicle(self, plate_number, exit_time=None):
        self.remove_from_parking(plate_number, exit_time)


class TimeService(TimeRangesDatabase):
    """This class will provide methods for working with dates and times,
    such as calculating the duration of a vehicle's stay in the parking lot."""

    def __init__(self):
        super().__init__()

    def get_vehicle_time_for_shift(self, license_plate):
        return self.get_ranges(license_plate)


class PaymentService(PaymentDatabase):
    """This class will be responsible for calculating the amount owed for parking."""

    def __init__(self):
        super().__init__()

    def get_amount_owed_without_discount(self, license_plate):
        shifts = TimeService().get_vehicle_time_for_shift(license_plate)
        amount_owed = 0

        for shift, hours in shifts.items():
            amount_owed += self.get_vehicle_rate_for_shift(shift, license_plate) * hours
        return amount_owed

    def get_amount_owed_with_discount(self, license_plate):
        amount = self.get_amount_owed_without_discount(license_plate)
        amount *= self.get_discount_rate(license_plate)
        return amount


class ExceptionHandling:
    """The service layer should include appropriate exception handling to handle errors
    and unexpected situations that may arise during the course of the application's operation."""


print(PaymentService().get_amount_owed_without_discount("CA1263HA"))
print(PaymentService().get_amount_owed_with_discount("CA1263HA"))
# car1 = Vehicle("A", "CA1263HA", "2022-03-01 16:30:00", "Silver")
# car2 = Vehicle("B", "CA4121HA", "2022-03-02 10:30:00", "Gold")
# car3 = Vehicle("B", "CA41212HA", "2022-03-02 10:30:00", "Gold")
# car4 = Vehicle("A", "CA4dwa12HA", "2022-05-02 10:30:00", "Gold")
# car5 = Vehicle("A", "CA4dwa1wad2HA", "2022-05-02 10:30:00", "Gold")
# car6 = Vehicle("A", "CA4ad2HA", "2022-05-02 12:30:00", "Gold")
# car7 = Vehicle("A", "CA412414ad2HA", "2022-05-02 12:30:00", "Mold")
# #
# ParkingLotService().add_vehicle(car1)
# ParkingLotService().add_vehicle(car2)
# # ParkingLotService().ParkingDB.cursor.execute(f'''UPDATE parking_lot_size SET available_area = 1 WHERE id = 1''')

# ParkingLotService().add_vehicle(car3)
# ParkingLotService().add_vehicle(car4)
# ParkingLotService().add_vehicle(car5)
# ParkingLotService().add_vehicle(car6)
# ParkingLotService().add_vehicle(car7)
# ParkingLotService().remove_vehicle("CA1263HA", "2022-03-02 00:30:00")
# ParkingLotService().remove_vehicle("CA4121HA", "2022-03-03 23:30:00")
# ParkingLotService().remove_vehicle("CA4ad2HA", "2022-05-03 1:30:00")
# ParkingLotService().remove_vehicle("CA41212HA", "2022-03-05 00:30:00")
# ParkingLotService().remove_vehicle("CA4dwa12HA", "2022-05-03 22:32:00")
# ParkingLotService().remove_vehicle("CA4dwa1wad2HA", "2022-05-02 10:34:00")
# ParkingLotService().remove_vehicle("CA412414ad2HA", "2022-12-12 22:30:00")

# print(TimeService().get_vehicle_time("CA1263HA"))
