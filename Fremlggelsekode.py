from w1thermsensor import W1ThermSensor, Sensor
from pushbullet import Pushbullet
from time import sleep
import datetime
import xlsxwriter

#Pushbullet setup
api_key = "o.ykiq6A2AgwYXbwuwhhnrCukyKBvsFmkU"
pb=Pushbullet(api_key)

#Kalder listen af enheder der er forbundet med samme API_KEY, da jeg kun har 1 enhed, bruger jeg bare den første den finder
phone = pb.devices[0]


#Excel config
datalog = xlsxwriter.Workbook("datalog2.xlsx")

wb = datalog.add_worksheet()

#Definere Row og Column, så jeg kan ændre på dem globalt
row = 0
column = 0

#Startformat til Excel fil
wb.write(0, 0, "Sensor 1")
wb.write(0, 1, "Sensor 2")
wb.write(0, 2, "Timestamp")


#Timer
timer = 0
timer3 = 0

#Bruger try, for at kunne afbryde programmet nemt med et KeyboardInterrupt
try:
    while True:
        #Sørger for at programmet kun spytter data ud, hver halve minut
        if timer < 1:

                row = row+1

                #Definere sensorene ud fra deres unikke ID
                sensor1 = W1ThermSensor(Sensor.DS18B20, "012275e4ad10")
                sensor2 = W1ThermSensor(Sensor.DS18B20, "012275b89bb2")

                #Får temperaturen, og laver dem til en variable jeg kan kalde på
                temp1 = (sensor1.get_temperature())
                temp2 = (sensor2.get_temperature())

                #Regner temperaturforskellen ud
                tempDiff = round(int(temp1)) - round(int(temp2))

                #Hvis temperaturforskellen er over 3 grader Celcius, ville den start en timer som kun stopper, hvis temperaturforskellen falder under 3 grader
                if tempDiff >= 3:
                    #Ser om temperaturforskellen er over 5, for at ungå notifikationer når brugeren bruger håndvasken i længere tid
                      if tempDiff > 5:
                          timer3 = 0
                          #Hvis temperatureforskellen stadig er mellem 3 og 5 grader i mere end (5 sekunder her), så får brugeren notifikation om vandspild
                          if timer3 >= 5:
                              push = phone.push_note("Måleenhed", "Der er vandspild")
                              timer3 = 0
                              sleep(5)
                          else:
                             timer3 = timer3+1
                             sleep(1)

                #Ekstra linje i tilfædet af TempDiff er negativ
                elif tempDiff < 0:
                    tempDiff = tempDiff * -1
                    
                else:
                    timer3 = 0
                    pass

                #Finder tidspunktet ud fra Raspberry Pi'ens klok
                now = datetime.datetime.now()

                #Sætter formatering af timestamp op
                date_time = now.strftime("%Y/%m/%d, %H:%M:%S")

                #Laver en variable der indholder temperatur + timestamp
                tempR = str(temp1), str(temp2), date_time + "\n"
                print(tempR, timer3)
                
                #Skriver data ud til Excel filen
                wb.write(row, column, temp1)
                wb.write(row, column+1, temp2)
                wb.write(row, column+2, date_time)

                timer = timer + 1
        else:
            sleep(10)
            timer = 0
            if timer3 > 0:
                timer3 = timer3+10
            else:
                pass

except KeyboardInterrupt:
    pass

#Lukker Excel filen
datalog.close()
