from datetime import timedelta, date
import json
from collections import defaultdict

def get_idling_date():
     
    last_week = date.today() - timedelta(days=7)
    day_number = date.isoweekday(last_week) 

    monday = last_week - timedelta(days=(day_number-1))
    tuesday = last_week - timedelta(days=(day_number-2))
    wednesday = last_week - timedelta(days=(day_number-3))
    thursday = last_week - timedelta(days=(day_number-4))
    friday = last_week - timedelta(days=(day_number-5))
    saturday = last_week - timedelta(days=(day_number-6))

    list = [monday, tuesday, wednesday, thursday, friday, saturday]

    return  list


def get_idling_endpoint(dates):

    list = []
    for i in dates:
        url = f"https://api.eu.samsara.com/fleet/reports/vehicle/idling?startTime={i}T00%3A00%3A00Z&endTime={i}T23%3A59%3A59Z&isPtoActive=false"
        list.append(url)
    return list


def get_idling_reports(list_endpoints):
    
    list_immat = []
    list_idlings = []

    for i in list_endpoints:
        list = []
        for j in i:
            try:
                immat = j['vehicle']["name"]
                if immat not in list_immat: list_immat.append(immat)
                duration = j["durationMs"]
                fuel = j["fuelConsumptionMl"]
                fuel = round(fuel / 1000, 2)

                set = {
                "Immatriculation" : immat,
                "Durée d'arrêt" : duration,
                "Carburant gaspillé" :  fuel
                }
                list.append(set)

            except Exception as e:
                print(f"Error: {type(e).__name__}: {e}")
                continue

        list_idlings.append(list)

    return list_idlings, list_immat


def compute_idling_reports(idling):

    grouped = defaultdict(lambda: {"duration": 0, "fuel": 0})

    for sublist in idling:
        for item in sublist:
            immat = item["Immatriculation"]
            grouped[immat]["duration"] += item["Durée d'arrêt"]
            grouped[immat]["fuel"] += item["Carburant gaspillé"]

    idling_computed = []

    for immat, values in grouped.items():
        duration = (values["duration"] / 1000) / 86400
        #duration = str(pd.Timedelta(duration).round("1s"))[7:15]

        idling_computed.append({
            "Immatriculation": immat,
            "Durée d'arrêt": duration,
            "Carburat gaspillé": values["fuel"]
        })

    return idling_computed

