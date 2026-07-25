import os
import requests
import json
from datetime import datetime, timedelta
from stop import Stop
from pprint import pprint
from prediction import Prediction
from stop import Stop
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("TRANSIT_API_KEY")  # Get the API key from environment variable

if not api_key:
    raise ValueError("API key not found. Please set the TRANSIT_API_KEY environment variable in the .env file.")

#agency can be switched to accomodate between Caltrain (CT) and ACE (CE) and VTA (SC)
#(stop_time_url).ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit returns a list of objects ()
#   -  [0].RecordedAtTime returns timestamp of when the data was recorded
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.ExpectedArrivalTime returns expected arrival time
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.ExpectedDepartureTime returns expected departure time
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.AimedArrivalTime returns aimed arrival time
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.AimedDepartureTime returns aimed departure time

#   -  [0]["MonitoredVehicleJourney"].LineRef returns line of transportation (ex. 522 for VTA)


#(base_url).Siri.ServiceDelivery.DataObjectDelivery.dataObjects.SiteFrame.stopPlaces.StopPlace returns a list of objects ()
# - [0].@id returns stop id
# - [0].name returns stop title 
# - timestamps

def get_data(id, stop_code):
    stripped_id = id.strip().upper()
    stop_time_url = f"https://api.511.org/transit/StopMonitoring?api_key={api_key}&agency={stripped_id}&stopcode={stop_code}&format=json"

    #REQUIRED: Add code here
    stop = Stop(stop_id=stop_code, operator_id=stripped_id)

    time_response = requests.get(stop_time_url, timeout=20)
    if time_response.status_code == 200:
        data = json.loads(time_response.content.decode("utf-8-sig"))
        get_timestamps(data, stop)
    return stop


def get_timestamps(data, stop: Stop):
    visits = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    # for i in range(100):
    #     journey = stopPlaces[i]["MonitoredVehicleJourney"]
    #     call = journey["MonitoredCall"]
    #     if call["ExpectedArrivalTime"] is None:
    #         continue
    #     expectedArrivalTime = datetime.fromisoformat(call["ExpectedArrivalTime"].replace("Z", "+00:00"))
    #     now = datetime.now(expectedArrivalTime.tzinfo)
    
    #     eta = expectedArrivalTime - now

    #     if call["StopPointName"] not in listOfStops:
    #         listOfStops[call["StopPointName"]] = {}

    #     listOfStops[call["StopPointName"]][journey["OriginName"]] = str(eta.total_seconds())
    
    for visit in visits:
        journey = visit["MonitoredVehicleJourney"]
        line_ref = journey["LineRef"]
        call = journey["MonitoredCall"]
        eta = call["ExpectedArrivalTime"]
        if call["ExpectedArrivalTime"] is None:
            continue
    
        arrival_time = datetime.fromisoformat(eta.replace("Z", "+00:00"))

        matching_prediction = next((p for p in stop.predictions if p.route == line_ref), None)

        if matching_prediction is not None:
            matching_prediction.arrival_times.append(arrival_time)
        else:
            stop.predictions.append(Prediction(route=line_ref, arrival_times=[arrival_time]))

        # expectedArrivalTime = datetime.fromisoformat(eta.replace("Z", "+00:00"))
        # now = datetime.now(expectedArrivalTime.tzinfo)
        # seconds = expectedArrivalTime - now



        

#Main function
id = input("Name your public transit agency pwease: ").strip().upper()
stop_code = input("Enter stop code pwease: ").strip()
pprint(get_data(id, stop_code))




