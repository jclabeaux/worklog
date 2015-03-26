#!/usr/bin/python
from datetime import datetime

clockIn = []
clockOut = []
now = datetime.now()
weekBegin = now.replace(day=(now.day - now.weekday()),hour=0,minute=0,second=0,microsecond=0)
nextClock = "IN"

for line in open("worklog.txt"):
    # Only read for the week
    lineTime = datetime.strptime(line.strip("INOUT ").rstrip(),"%m-%d-%Y %H.%M")
    if(lineTime < weekBegin):
        continue

    # Read punch in/out card
    if nextClock is "IN":
        if "OUT" in line:
            print("Clocking Error, expecting clockIN")
            break
        if "IN" not in line:
            continue
        else:
            clockIn.append(lineTime)
            nextClock = "OUT"
            continue
    elif nextClock is "OUT":
        if "IN"  in line:
            print("ClockingError, expected clockOUT")
            break
        if "OUT" not in line:
            continue
        else:
            clockOut.append(lineTime)
            nextClock = "IN"
            continue

# Strip out unmatched clockIN
if(len(clockIn) > len(clockOut)):
        clockIn.pop()

# Reset Weeklog
weekLog = clockIn[0] - clockIn[0]

# Each day of the week
for day in range(0,7):
    printDay = "None" 

    # Reset Daylog
    dayLog = clockIn[0] - clockIn[0]

    # Scan log for all times relating to that day
    for idx in range(len(clockIn)):

        if(clockIn[idx].weekday() == day):
            dayLog += (clockOut[idx] - clockIn[idx])
            printDay = clockIn[idx].strftime("%A")

    if printDay is not "None":
        dayHr,remainder = divmod(dayLog.seconds, 3600)
        dayMin,daySec = divmod(remainder, 60)
        print(printDay + " total hours - %d:%d" % (dayHr, dayMin) )
        weekLog += dayLog
        
print("-------------------------------")
weekHr,remainder = divmod(weekLog.seconds, 3600)
weekMin,weekSec = divmod(remainder, 60)
weekHr += (24*weekLog.days)
print("Week total hours - %d:%d" % (weekHr, weekMin) )
