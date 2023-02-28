from data_level import TimeRangesDatabase
from data_level.database_setup import DatabaseCon


class PaymentDatabase(DatabaseCon):

    def __init__(self):
        super().__init__()


    def get_amount_owed(self,license_plate):
        pass

