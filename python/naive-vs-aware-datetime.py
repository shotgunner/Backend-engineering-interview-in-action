# the difference between naive and aware datetime

from datetime import datetime, timezone, timedelta

naive_datetime = datetime(2024, 11, 17, 10, 0, 0)
print(naive_datetime)

# will print 2024-11-17 10:00:00

iran_timezone = timezone(timedelta(hours=3, minutes=30))

aware_datetime = datetime(2024, 11, 17, 10, 0, 0, tzinfo=iran_timezone)
print(aware_datetime)

# will print 2024-11-17 10:00:00+03:30
