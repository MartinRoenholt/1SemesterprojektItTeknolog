from w1thermsensor import W1ThermSensor, Sensor
from pushbullet import Pushbullet
from time import sleep
import datetime
import xlsxwriter

#Pushbullet setup
api_key = "o.keqGxblYYBvR5jRVObIWjEgUfyVdPR9P"
pb=Pushbullet(api_key)

phone = pb.devices[0]


#Excel config
datalog = xlsxwriter.Workbook("datalog2.xlsx")

wb = datalog.add_worksheet()

row = 0
column = 0

wb.write(0, 0, "Sensor 1")
wb.write(0, 1, "Sensor 2")
wb.write(0, 2, "Timestamp")


#Timer
timer = 1
timer2 = 0
timer3 = 0

try:
    while True:
        if timer2 >= 1024:
            push = phone.push_note("Målenehed", "Programmet kører stadig")
            timer2 = 0

        elif timer < 2:

                sensor1 = W1ThermSensor(Sensor.DS18B20, "012275e4ad10")
                sensor2 = W1ThermSensor(Sensor.DS18B20, "012275b89bb2")

                row = row+1

                temp1 = (sensor1.get_temperature())
                temp2 = (sensor2.get_temperature())

                tempDiff = round(int(temp1)) - round(int(temp2))
                if tempDiff >= 3:
                    if timer3 >= 30:
                        push = phone.push_note("Måleenhed", "Der er vandspild")
                        timer3 = 0
                        sleep(5)
                    else:
                        timer3 = timer3+1
                else:
                    pass


                now = datetime.datetime.now()
                date_time = now.strftime("%Y/%m/%d, %H:%M:%S")
                tempR = str(temp1), str(temp2), date_time + "\n"
                print(tempR)
                
                wb.write(row, column, temp1)
                wb.write(row, column+1, temp2)
                wb.write(row, column+2, date_time)

                timer = timer + 1
                timer2 = timer2 + 1
        else:
            sleep(30)
            timer = 0
            timer2 = timer2 + 30

except KeyboardInterrupt:
    pass
datalog.close()