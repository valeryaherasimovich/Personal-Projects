!pip install xmltodict
import requests
import google.colab.files
import csv
import json
import datetime
import xmltodict
import os
#This code will output realtime data for each earthquake that occurs in the United States or off the coast.
#The data that will be collected and presented will be the earthquake's magnitude, date and time, coordinates, and the location.
times = []
if os.path.exists("earthquakes.csv"):
  with open("earthquakes.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
      times.append(row[0])

response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson")

if response:
  data = json.loads(response.text)

  for i in data["features"]:
    orig_time = i["properties"]["time"]
    #Convert milliseconds to seconds
    orig_time_sec = orig_time / 1000
    #Convert Unix epoch time to datetime object
    datetime_timestamp = datetime.datetime.utcfromtimestamp(orig_time_sec)
    #Subtract 7 hours to adjust for time zone difference
    datetime_adj_timestamp = datetime_timestamp - datetime.timedelta(hours = 7)
    #Convert to human-interpretable string
    #String would say: “September 01, 2021 at 12:00:00 AM”
    time_str = datetime_adj_timestamp.strftime("%B %d, %Y at %I:%M:%S %p")
    #Get magnitude and coordinates
    mag = i["properties"]["mag"]
    longitude = i["geometry"]["coordinates"][0]
    latitude = i["geometry"]["coordinates"][1]
    response = requests.get("https://api.opencagedata.com/geocode/v1/xml?q="+str(latitude)+"+"+str(longitude)+"&key=9095fdba3c764ff3bf4daa5caba72d55")
    if response:
      data = xmltodict.parse(response.text)
      #Get county and state
      if "county" in data["response"]["results"]["result"]["components"]:
        county = data["response"]["results"]["result"]["components"]["county"]
        state = data["response"]["results"]["result"]["components"]["state"]
        print("Magnitude", mag, "earthquake on", time_str,"and located at (",longitude,"," , latitude,")", "in", county, "," , state)
      #If location isn't within United States
      else:
        print("Magnitude", mag, "earthquake on", time_str,"and located at (",longitude,"," , latitude,")", "in Ocean")
        county = "N/A"
        state = "N/A"
      with open("earthquakes.csv", "a") as file:
        writer = csv.writer(file)
        #Write into CSV file
        if time_str not in times:
          writer.writerow([time_str, mag, longitude, latitude, county, state])
    else:
      print("Sorry, connection error.")
else:
  print("Sorry, connection error.")
