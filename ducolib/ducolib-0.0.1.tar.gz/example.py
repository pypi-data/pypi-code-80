import ducolib
import time

# Mining for 30 seconds
workers=ducolib.MinerCrewChief('Alicia426',True,'auto')
workers.start_mining()
time.sleep(10)
print(workers.check_status())
time.sleep(10)
print(workers.check_status())
workers.stop_mining()
