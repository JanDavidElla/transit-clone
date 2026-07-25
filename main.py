import requests
import json
from datetime import datetime, timedelta
from stop import Stop
from pprint import pprint

base_url = "https://api.511.org/transit/stopplaces?api_key=1b477b94-510b-4227-a5c2-b8436f015197&operator_id=CT&format=json"
stop_time_url = "https://api.511.org/transit/StopMonitoring?api_key=1b477b94-510b-4227-a5c2-b8436f015197&agency=CT&format=json"
#agency can be switched to accomodate between Caltrain (CT) and ACE (CE) and VTA (SC)
#(stop_time_url).ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit returns a list of objects ()
#   -  [0].RecordedAtTime returns timestamp of when the data was recorded
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.ExpectedArrivalTime returns expected arrival time
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.ExpectedDepartureTime returns expected departure time
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.AimedArrivalTime returns aimed arrivalhttps://api.511.org/transit/stopplaces?api_key=1b477b94-510b-4227-a5c2-b8436f015197&operator_id=CT&format=json time
#   -  [0]["MonitoredVehicleJourney"].MonitoredCall.AimedDepartureTime returns aimed departure time

#   -  [0]["MonitoredVehicleJourney"].LineRef returns line of transportation (ex. 522 for VTA)


#(base_url).Siri.ServiceDelivery.DataObjectDelivery.dataObjects.SiteFrame.stopPlaces.StopPlace returns a list of objects ()
# - [0].@id returns stop id
# - [0].name returns stop title 
# - timestamps

def get_data(id):
    stripped_id = id.strip().upper()
    base_url = f"https://api.511.org/transit/stopplaces?api_key=1b477b94-510b-4227-a5c2-b8436f015197&operator_id={stripped_id}&format=json"
    stop_time_url = f"https://api.511.org/transit/StopMonitoring?api_key=1b477b94-510b-4227-a5c2-b8436f015197&agency={stripped_id}&format=json"
    list = []

    #REQUIRED: Add code here
    name_response = requests.get(base_url)
    print(name_response.url)
    if name_response.status_code == 200: 
        data = json.loads(name_response.content.decode("utf-8-sig"))

        stopPlaces = data["Siri"]["ServiceDelivery"]["DataObjectDelivery"]["dataObjects"]["SiteFrame"]["stopPlaces"]["StopPlace"]
        print(stopPlaces[0]["@id"])
    else:
        print('data not found')

    time_response = requests.get(stop_time_url, timeout=20)
    if time_response.status_code == 200:
        data = json.loads(time_response.content.decode("utf-8-sig"))
        get_timestamps(data)

def get_timestamps(data):
    # for i in range(100):
    #     stopPlaces = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    #     journey = stopPlaces[i]["MonitoredVehicleJourney"]
    #     monitoredCall = journey["MonitoredCall"]
    #     if monitoredCall["ExpectedArrivalTime"] is None:
    #         print("this one has nothing available")
    #         continue
    #     expectedArrivalTime = datetime.fromisoformat(monitoredCall["ExpectedArrivalTime"].replace("Z", "+00:00"))
    #     now = datetime.now(expectedArrivalTime.tzinfo)
    
    #     eta = expectedArrivalTime - now
    #     if int(eta.total_seconds()) <= 0:
    #         print('it has already arrived!')
    #     else: 
    #         if journey['OriginName'] != None:
    #             print("Transportation from " + journey['OriginName'] + " is expected to arrive at " + monitoredCall["StopPointName"] + " in " + str(eta.total_seconds()) + " seconds")

    stopPlaces = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    for i in range(100):
        journey = stopPlaces[i]["MonitoredVehicleJourney"]
        call = journey["MonitoredCall"]
        if call["ExpectedArrivalTime"] is None:
            continue
        expectedArrivalTime = datetime.fromisoformat(call["ExpectedArrivalTime"].replace("Z", "+00:00"))
        now = datetime.now(expectedArrivalTime.tzinfo)
    
        eta = expectedArrivalTime - now

        if call["StopPointName"] not in listOfStops:
            listOfStops[call["StopPointName"]] = {}

        listOfStops[call["StopPointName"]][journey["OriginName"]] = str(eta.total_seconds())



        #dictionary of dictionaries
        # listOfStops = {onestop: {fromThis: time, fromThis: time},
        #                }


    
    
    



#Main function
listOfStops = {}
id = input("Name your public transit agency pwease: ").strip().upper()
stop = input("Name your stop pwetty pwease: ")
get_data(id)
pprint(listOfStops)



