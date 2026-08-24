import os
import xlwings as xw
from dotenv import load_dotenv
from src.vehicle import *
from src.gateway import *
from src.fetch import *
from src.fuel import *
from src.tachy import *
from src.maintenance import *
from src.idling import *
from datetime import date, timedelta, time
import pandas as pd
import requests

load_dotenv()

start_date = get_last_week_date()
end_date = start_date + timedelta(days=5)
api_key = os.getenv("API_KEY")

url_vehicles = "https://api.eu.samsara.com/fleet/vehicles" # List of Samsara Parc
url_gateway = "https://api.eu.samsara.com/gateways" #List of all gateways (boitiers)
url_fuel = f"https://api.eu.samsara.com/fleet/reports/vehicles/fuel-energy?startDate={start_date}T00%3A00%3A00.000Z&endDate={end_date}T23%3A59%3A59Z"
url_tachy = f"https://api.eu.samsara.com/fleet/vehicles/tachograph-files/history?startTime={start_date}T00%3A00%3A00Z&endTime={end_date}T23%3A59%3A59Z"

headers = {
    "accept" : "application/json",
    "authorization" : "Bearer " + api_key
}
params = {}

columns = [
    "Immatriculation", 
    "id",
    "Vehicule",
    "TRS",
    "Site", 
    "VIN", 
    "Boitier", 
    "Model", 
    "Fichier Tachy", 
    "Efficacite", 
    "Abusif",
    "Carburant consomme", 
    "Distance parcouru", 
    "Emission de carbonne",
    "Semaine", 
    "Durée d'arrêt",
    "Carburat gaspillé",
    "site",
    "Etat",
    "Famille",
    "Vendu",
    "Erreur Immat",
    "OFF",
    "MIL",
    "AWL",
    "RSL"
]
    
columns2 = [
    "Boitier",
    "Model",
    "VIN",
    "Status",
    "Last connection",
    "Etat",
    "Installé"
]


def fetch_all_pages(url):

    list = []
    hasNextPage = True
    try :
        while hasNextPage :

            response = requests.get(url=url, headers=headers, params=params).json() # type: ignore
            if "fuel" in url:
                for i in response["data"]["vehicleReports"]:
                    list.append(i)
                hasNextPage = response["pagination"]["hasNextPage"]
                params["after"] = response["pagination"]["endCursor"] #type
            else :
                for i in response["data"]:
                    list.append(i)
                hasNextPage = response["pagination"]["hasNextPage"]
                params["after"] = response["pagination"]["endCursor"] 
    except:
        response = requests.get(url=url, headers=headers, params=params).json()
        for i in response["data"]:
                list.append(i)
    return list


def fetch_fuel(url, headers):

    while True:  #Loop for retries
        response = requests.get(url, headers=headers)
        
        if response.status_code != 429:  #Status other than 'Too Many Requests'
            return response
        
        #Encountered rate limit, get the time to wait from the 'Retry-After' header
        retry_after = float(response.headers.get('Retry-After', 1))  #Default to 1 second if header is missing
        
        print(f"Rate limit exceeded. Retrying in {retry_after} seconds.")
        
        # Wait for the duration specified in 'Retry-After' before making another request
        time.sleep(retry_after)


def fetch_all_endpoints(endpoints):

    list_response = []
    for i in endpoints:
        response = fetch_all_pages(i)
        list_response.append(response)
    return list_response


if __name__ == "__main__":

    wb = xw.Book("TDB Samsara.xlsm")
    
    sip2 = get_national_parc() # type: ignore
    site_samsara, site_SIP2 = get_platform()
    active_gateway = get_gateway_status()
    dates = get_idling_date()

    endpoints = get_idling_endpoint(dates)

    response_gateway = fetch_all_pages(url_gateway)
    list_response_idling = fetch_all_endpoints(endpoints)
    response_vehicle = fetch_all_pages(url_vehicles) 
    response_fuel = fetch_all_pages(url_fuel) 
    response_tachy = fetch_all_pages(url_tachy)
    
    gateway = get_all_gateway(response_gateway)
    vehicles = get_vehicles_info(response_vehicle)
    vehicles = duplicated_vehicles(vehicles)
    missing_fuel, abusive_fuel, fuel = get_fuel_info(response_fuel)
    tachy = get_tachy_files(response_tachy)
    gateway_ordered = get_ordered_gateway()
    idling, immats = get_idling_reports(list_response_idling)
    idling_computed = compute_idling_reports(idling)
    alerts = get_vehicles_alerts()
    alerts = get_new_alerts_array(alerts)
    alerts = get_alerts_site(alerts, site_samsara)

    bis = gather_data(gateway_ordered, gateway, "Boitier")
    join_vehicles = gather_data(vehicles, tachy, "Immatriculation")
    main = gather_data(join_vehicles, fuel, "Immatriculation")
    main = gather_data(main, idling_computed, "Immatriculation")
    
    main = get_correspondant_site(main, site_samsara, site_SIP2)
    main = get_health_status(main, active_gateway)
    main = get_vehicle_segment(main, sip2)
    main = is_vehicle_sold(main, sip2)
    main = immat_error(main, sip2)
    main = join_alerts(main, alerts)

    bis = get_health_status(bis, active_gateway)
    bis = isInstalled(bis)

    parc = get_parc_window(sip2)
    
    dt1 = pd.DataFrame(main, columns=columns)
    dt2 = pd.DataFrame(bis)
    dt3 = pd.DataFrame(parc)

    sheet1 = wb.sheets["Consommations & Tachy"]
    sheet2 = wb.sheets["Boitiers"]
    sheet3 = wb.sheets["Parc SIP2"]
    sheet1.range("A1").options(index=False).value = dt1
    sheet2.range("A1").options(index=False).value = dt2
    sheet3.range("A1").options(index=False).value = dt3

    wb.save()
    wb.close