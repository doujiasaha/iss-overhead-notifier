import requests
from datetime import datetime
import smtplib
import time

MY_LAT = -7.520008 # Your latitude
MY_LONG = 5.404954 # Your longitude

def is_iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    
    print(iss_latitude)
    print(iss_longitude)
    
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        print("Currently ISS is in viscinity")
        return True


#Your position is within +5 or -5 degrees of the ISS position.




def is_it_dark():
    parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    #is_time_in_range(time_now.hour, sunset, sunrise)
  

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

def is_time_in_range(hour, start, end):
    if start <= end:
        return start <= hour < end
    else:
        # crosses midnight
        return hour >= start or hour < end


secrets = {}

with open("secret.txt","r") as secret:
    for line in secret:
        line = line.strip()
        if not line:
            continue
        key, value = line.split("=", 1)
        secrets[key.strip()] = value.strip()


my_email = secrets.get("my_email")
password = secrets.get("password")
to_adress = secrets.get("to_address")


while True:
    print("Searching for ISS coordinates...")    

    if is_iss_overhead() and is_it_dark():
        with smtplib.SMTP("smtp.gmail.com",587) as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email, 
                to_addrs=to_adress, 
                msg=f"Subject: ISS near you! \n\nLOOK UP!"
                )
            print("Email sent successfully.")
    print("Waiting 60 seconds...")
    time.sleep(60)
