import requests

base_url = "https://api.511.org/transit/stopplaces?api_key=1b477b94-510b-4227-a5c2-b8436f015197&operator_id=CT&format=json"
stop_time_url = "https://api.511.org/transit/StopMonitoring?api_key=1b477b94-510b-4227-a5c2-b8436f015197&agency=CT&format=json"
#agency can be switched to accomodate between Caltrain (CT) and ACE (CE) and VTA (SC)
#data.ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit returns a list of objects ()
# - .@id returns stop id
# - .name returns stop title 
# - timestamps

def get_stuffs(url):
    pass

get_stuffs()