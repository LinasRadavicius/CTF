import random
import time
from datetime import datetime

known_time = "2025-04-05 21:10:42"
timestamp = int(time.mktime(datetime.strptime(known_time, "%Y-%m-%d %H:%M:%S").timetuple()))

random.seed(timestamp)

NUMBERS = '0123456789'
password_generate = ''.join(random.choice(NUMBERS) for _ in range(32))

print(password_generate)
