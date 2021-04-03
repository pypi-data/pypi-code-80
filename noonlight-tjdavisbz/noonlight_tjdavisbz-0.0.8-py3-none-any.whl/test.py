from noonlight import Noonlight

alarm = Noonlight("https://api-sandbox.noonlight.com/dispatch/v1/alarms","gSwrpftjAUvcQPRJK9R1oF8Ia2vPCYU8")

response = alarm.createAlarm("1000 Copper Canyon Rd","Argyle","TX","76226",True,False,False,False,"Gate Code #02745","TJ Davis","12149493568","9403")

print(alarm.status)
#print(alarm.alarmID)