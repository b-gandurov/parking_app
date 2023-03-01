from data_level.database_setup import DatabaseCon


class PaymentDatabase(DatabaseCon):

    def __init__(self):
        super().__init__()

    def get_vehicle_rate_for_shift(self, rate_type, license_plate):
        rate_check = self.get_item("rate_type", "rate_types", "rate_type", rate_type)
        vehicle_type = self.get_item("type_vehicle", "vehicles", "plate_number", license_plate)
        return self.get_item("rate", rate_check, "vehicle", vehicle_type)

    def get_discount_rate(self, license_plate):
        assigned_discount = self.get_item("discount", "vehicles", "plate_number", license_plate)
        try:
            discount_rate = self.get_item("rate","discount","type",assigned_discount)
        except Exception:
            return 1
        return 1-discount_rate

#
# print(PaymentDatabase().get_discount_rate("CA412414ad2HA"))
# print(PaymentDatabase().get_vehicle_rate_for_shift("night_hours","CA412414ad2HA"))
