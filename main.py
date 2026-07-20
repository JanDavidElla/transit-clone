import requests

base_url = "https://api.511.org/transit/stopplaces?api_key=1b477b94-510b-4227-a5c2-b8436f015197&operator_id=CT&format=json"
stop_time_url = "https://api.511.org/transit/StopMonitoring?api_key=1b477b94-510b-4227-a5c2-b8436f015197&agency=CT&format=json"
#agency can be switched to accomodate between Caltrain (CT) and ACE (CE) and VTA (SC)
#(stop_time_url).ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit returns a list of objects ()
#   -  .RecordedAtTime returns timestamp of when the data was recorded
#   -  .MonitoredCall.ExpectedArrivalTime returns expected arrival time
#   -  .MonitoredCall.ExpectedDepartureTime returns expected departure time
#   -  .MonitoredCall.AimedArrivalTime returns aimed arrivalhttps://api.511.org/transit/stopplaces?api_key=1b477b94-510b-4227-a5c2-b8436f015197&operator_id=CT&format=json time
#   -  .MonitoredCall.AimedDepartureTime returns aimed departure time


#(base_url).Siri.ServiceDelivery.DataObjectDelivery.dataObjects.SiteFrame.stopPlaces.StopPlace returns a list of objects ()
# - [0].@id returns stop id
# - [0].name returns stop title 
# - timestamps

def get_timestamps(stop, id):
    base_url = f"https://api.511.org/transit/stopplaces?api_key=1b477b94-510b-4227-a5c2-b8436f015197&operator_id={id}&format=json"
    stop_time_url = f"https://api.511.org/transit/StopMonitoring?api_key=1b477b94-510b-4227-a5c2-b8436f015197&agency={id}&format=json"
    list = []

    #REQUIRED: Add code here

    
    return list



#sample code
id = input("Name your public transit agency pwease: ")
stop = input("Name your stop pwetty pwease: ")
get_timestamps(stop, id)



