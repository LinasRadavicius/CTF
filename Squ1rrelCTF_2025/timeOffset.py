import random
import time
from datetime import datetime, timedelta

known_time = "2025-04-05 21:10:42"
base_timestamp = int(time.mktime(datetime.strptime(known_time, "%Y-%m-%d %H:%M:%S").timetuple()))
passwords = []
NUMBERS = '0123456789'

for offset in range(-30, 31):  # From -30 to +30 seconds
    test_timestamp = base_timestamp + offset
    random.seed(test_timestamp)
    password = ''.join(random.choice(NUMBERS) for _ in range(32))
    print(password)
    passwords.append(password)
with open("timestamp.txt", "w") as f:
    for pw in passwords:
        f.write(pw + '\n')
