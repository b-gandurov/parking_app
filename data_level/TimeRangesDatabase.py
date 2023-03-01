import math
from datetime import datetime, timedelta
from data_level.database_setup import DatabaseCon


class TimeRangesDatabase(DatabaseCon):

    def __init__(self):
        super().__init__()

    def get_vehicle_start_end_time_in_datetime(self, license_plate) -> tuple[datetime, datetime]:
        start_time, end_time = self.cursor.execute(f"SELECT entered_at, exited_at FROM vehicles "
                                                   f"WHERE plate_number = ? "
                                                   f"ORDER BY entered_at DESC LIMIT 1", (license_plate,)).fetchone()
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        return start_time, end_time

    def get_time_frame_from_time(self, time: datetime):
        time = time.time()
        shifts = {row[0]: (datetime.strptime(row[1], '%H:%M:%S').time(), datetime.strptime(row[2], '%H:%M:%S').time())
                  for row in
                  self.cursor.execute("SELECT rate_type, start_time, end_time FROM rate_types").fetchall()}
        shifts_collection = []
        for shift, (start_time, end_time) in shifts.items():
            if start_time > end_time:
                if start_time <= time or time < end_time:
                    shifts_collection.append(shift)
            elif start_time <= time < end_time:
                shifts_collection.append(shift)
        return shifts_collection

    @staticmethod
    def get_next_time(time: datetime):
        time += timedelta(hours=1)
        return time

    def get_ranges(self, license_plate):
        ranges = {}
        start, end = self.get_vehicle_start_end_time_in_datetime(license_plate)
        while start < end:
            time_frame_collection = self.get_time_frame_from_time(start)
            for frame in time_frame_collection:
                if frame not in ranges:
                    ranges[frame] = 0
                ranges[frame] += 1
            start += timedelta(hours=1)
        return sum(ranges.values()), ranges


time = datetime.strptime('8:00:00', '%H:%M:%S')
print(TimeRangesDatabase().get_ranges("CA1263HA"))
print(TimeRangesDatabase().get_ranges("CA4121HA"))
print(TimeRangesDatabase().get_ranges("CA41212HA"))
print(TimeRangesDatabase().get_ranges("CA4dwa12HA"))
print(TimeRangesDatabase().get_ranges("CA4dwa1wad2HA"))
print(TimeRangesDatabase().get_ranges("CA4ad2HA"))
print(TimeRangesDatabase().get_ranges("CA412414ad2HA"))

# def calculate_hours(self, license_plate):
#     # Get start and end time from vehicles table
#     start_time, end_time = self.cursor.execute(f"SELECT entered_at, exited_at FROM vehicles "
#                                                f"WHERE plate_number = ? "
#                                                f"ORDER BY entered_at DESC LIMIT 1", (license_plate,)).fetchone()
#     start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
#     end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
#     # Get shift start and end times from rate_types table
#     shifts = self.cursor.execute("SELECT rate_type, start_time, end_time FROM rate_types").fetchall()
#
#     shift_hours = {}
#     for shift in shifts:
#         shift_hours[shift[0]] = 0
#
#     current_time = start_time
#     while current_time < end_time:
#         for shift in shifts:
#             shift_start = datetime.strptime(shift[1], "%H:%M:%S").time()
#             shift_end = datetime.strptime(shift[2], "%H:%M:%S").time()
#
#             # Calculate start and end times for current shift
#             if shift_start < shift_end:
#                 shift_start_time = datetime.combine(current_time.date(), shift_start)
#                 shift_end_time = datetime.combine(current_time.date(), shift_end)
#             else:
#                 # If shift crosses midnight, add 1 day to end time
#                 shift_start_time = datetime.combine(current_time.date(), shift_start)
#                 shift_end_time = datetime.combine(current_time.date() + timedelta(days=1), shift_end)
#
#             # Calculate hours in current shift
#             shift_duration = min(end_time, shift_end_time) - max(current_time, shift_start_time)
#             shift_hours[shift[0]] += shift_duration.total_seconds() / 3600.0
#
#         # Increment current_time to start of next day
#         current_time += timedelta(days=1)
#         current_time = datetime.combine(current_time.date(), datetime.min.time())
#
#     return shift_hours


#     def
#
#     def start_to_end_date(self, start: datetime, end: datetime):
#         shifts = {row[0]: (row[1], row[2]) for row in
#                   self.cursor.execute("SELECT rate_type, start_time, end_time FROM rate_types").fetchall()}
#         calculated_shifts = {}
#         print(shifts)
#         while start < end:
#             for shift in shifts:
#                 start_shift = datetime.strptime(shifts[shift][0], '%H:%M:%S')
#                 end_shift = datetime.strptime(shifts[shift][1], '%H:%M:%S')
#                 if start_shift.time() <= start.time():
#                     if start_shift.time() > end_shift.time():
#                         end_shift_1 = datetime.strptime("23:59:00", '%H:%M:%S').time()
#                         end_shift_2 = end_shift.time()
#                         start = start.time()
#                         time_diff_hours = (datetime.combine(datetime.min, end_shift_1) -
#                                            datetime.combine(datetime.min, start)).total_seconds() / 3600
#                         calculated_shifts[shift] = 0
#                         calculated_shifts[shift] += time_diff_hours
#                     # print("yes")
#
#         # print(start.time())
#         # print(end.time())
#
#
# TimeRangesDatabase().start_to_end_date(*TimeRangesDatabase().calculate_hours("CA1263HA"))
#
# # print(TimeRangesDatabase().calculate_hours("CA4121HA"))
# # print(TimeRangesDatabase().calculate_hours("CA1263HA"))
# # print(TimeRangesDatabase().calculate_hours("CA41212HA"))
# # print(max("2022-03-02 22:30:00", "2022-03-03 18:00:00"))
#

# shift_hours = {}
# types = self.cursor.execute("SELECT rate_type FROM rate_types")
# for type in types:
#     shift_hours[type[0]] = 0

# def get_exited_at(self, license_plate):
#     exited_at = self.cursor.execute(f"SELECT exited_at FROM vehicles "
#                                     f"where plate_number = {license_plate} "
#                                     f"ORDER BY entered_at DESC LIMIT 1").fetchone()[0]
#     return exited_at

# def get_rate_types(self):
#     rows = self.cursor.execute("SELECT rate_type, start_time, end_time FROM rate_types").fetchall()
#     rate_types = {}
#     for row in rows:
#         rate_type, start_time, end_time = row
#         rate_types[rate_type] = [start_time, end_time]
#     return rate_types

# def time_parked_for_each_rate(self, license_plate):
#     rates = {}
#     result = self.cursor.execute(f"SELECT entered_at, exited_at FROM vehicles "
#                                            f"where plate_number = ? "
#                                            f"ORDER BY entered_at DESC LIMIT 1", (license_plate,)).fetchall()[0]
#     print([x for x in result])
#     start, end = self.cursor.execute(f"SELECT entered_at, exited_at FROM vehicles "
#                                            f"where plate_number = ? "
#                                            f"ORDER BY entered_at DESC LIMIT 1", (license_plate,)).fetchall()[0]
#     rate_types = self.get_rate_types()
#     for rate, (start_time, end_time) in rate_types.items():
#         rate_hours = self.get_time_diff_in_hours(start_time, end_time, start, end)
#         rates[rate] = rate_hours
#     return rates

# @staticmethod
# def get_time_diff_in_hours(start_time, end_time, rate_start_time, rate_end_time):
#     start = datetime.strptime(max(start_time, rate_start_time), "%Y-%m-%d %H:%M:%S")
#     end = datetime.strptime(min(end_time, rate_end_time), "%Y-%m-%d %H:%M:%S")
#     diff = end - start
#     diff_in_seconds = diff.total_seconds()
#     diff_in_hours = math.ceil(diff_in_seconds / 3600)
#     return diff_in_hours


# class PaymentDatabase(DatabaseCon):
#     TimeDB = TimeRangesDatabase()
#
#     def __init__(self):
#         super().__init__()
#
#     def get_vehicle_type(self, license_plate):
#         return self.cursor.execute("SELECT * FROM vehicles WHERE plate_number = ?", (license_plate,)).fetchone()[0]
#
#     def get_amount_owed(self, license_plate):
#         ranges = self.TimeDB.time_parked_for_each_rate(license_plate)
#         vehicle_type = self.get_vehicle_type(license_plate)
#         owed = 0
#         for table_range in ranges:
#             amount = self.cursor.execute(f"SELECT rate FROM {table_range} WHERE vehicle = {vehicle_type}").fetchone()[0]
#             owed += amount * ranges[table_range]
#         return owed
