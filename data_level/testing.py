# from datetime import datetime, timedelta
#
# # Function to calculate the hours between two dates
# def calculate_hours(start_time, end_time, start_hour, end_hour):
#     shift_hours = {'day': 0, 'night': 0}
#
#     current_time = start_time
#     while current_time < end_time:
#         next_shift_start = datetime(
#             current_time.year,
#             current_time.month,
#             current_time.day,
#             end_hour,
#             0,
#             0
#         ) if current_time.hour < end_hour else datetime(
#             current_time.year,
#             current_time.month,
#             current_time.day,
#             start_hour,
#             0,
#             0
#         ) + timedelta(days=1)
#
#         # Calculate hours in current shift
#         shift_duration = min(end_time, next_shift_start) - current_time
#         shift_hours['day' if start_hour <= current_time.hour < end_hour else 'night'] += shift_duration.total_seconds() / 3600.0
#
#         current_time = next_shift_start
#
#     return shift_hours
#
#
# # Function to calculate parking cost based on shift hours
# def calculate_parking_cost(shift_hours, day_rate=10, night_rate=5):
#     total_cost = shift_hours['day'] * day_rate + shift_hours['night'] * night_rate
#     return total_cost
#
#
# start_time = datetime(2022, 3, 1, 14, 30)
# end_time = datetime(2023, 3, 2, 10, 30)
#
# shift_hours = calculate_hours(start_time, end_time)
# total_cost = calculate_parking_cost(shift_hours)
#
# print(shift_hours)  # {'day': 4.5, 'night': 6.5}
# print(total_cost)
#
#
#
