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
        return ranges


# time = datetime.strptime('8:00:00', '%H:%M:%S')
# print(TimeRangesDatabase().get_ranges("CA1263HA"))
# print(TimeRangesDatabase().get_ranges("CA4121HA"))
# print(TimeRangesDatabase().get_ranges("CA41212HA"))
# print(TimeRangesDatabase().get_ranges("CA4dwa12HA"))
# print(TimeRangesDatabase().get_ranges("CA4dwa1wad2HA"))
# print(TimeRangesDatabase().get_ranges("CA4ad2HA"))
# print(TimeRangesDatabase().get_ranges("CA412414ad2HA"))