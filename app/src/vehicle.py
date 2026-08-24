import pandas as pd
from .fuel import week
def get_vehicles_info(list):

    list_vehicle = []

    for i in list:
        immat = i["name"]
        id = i["id"]
        try :
            vin = i["vin"]
        except KeyError: 
            vin = None
        try :
            for j in i["tags"]:
                site = j["name"]
        except KeyError:
            site = None
        try : 
            gateway = i["gateway"]["serial"]
            model = i["gateway"]["model"]
        except KeyError:
            gateway = None
            model = None
        try:
            for j in i["attributes"]:
                if j["name"] == "TRS":
                    trs = j["stringValues"][0]
        except:
            trs = "N/A"

        if len(immat) == 9:
            vehicule = "Oui"
        else : vehicule = "Non"

        vehicle  = {
            "Immatriculation" : immat,
            "id" : id,
            "Vehicule" : vehicule,
            "TRS" : trs,
            "Site" : site,
            "VIN" : vin,
            "Boitier" : gateway,
            "Model" : model
        }  
        list_vehicle.append(vehicle) 
        
    return list_vehicle


def get_national_parc():

    dt = pd.read_excel("../ressource/Parc Nat.xlsx").to_dict(orient="records")

    return dt


def get_vehicle_segment(vehicle, parc):

    for i in vehicle:
        for j in parc:
            if i["Immatriculation"] == j['Immatriculation']:
                famille = j['Segment']
                break
            famille = "Pas sur SIP2"
        i.update({"Famille" : famille})

    return vehicle


def is_vehicle_sold(vehicle, parc):
    
    for i in vehicle:
        for j in parc:
            if i["Immatriculation"] == j["Immatriculation"]:
                sold = j["Date de retrait"]
                break
            else : sold = "Pas sur SIP2"
        i.update({"Vendu" : sold})

    return vehicle


def duplicated_vehicles(vehicle):
    
    final_list = []
    list_immat = []
    for i in vehicle:
        if i["Immatriculation"] in list_immat:continue
        for j in vehicle:
            if i["Immatriculation"] == j["Immatriculation"]:
                try:
                    if len(i["VIN"]) > len(j["VIN"]):
                        choice = i
                    elif len(i["Boitier"]) >= len (j["Boitier"]):
                        choice = i
                    else: choice = j
                except: choice = j
        final_list.append(choice)
        list_immat.append(choice["Immatriculation"])
        
    return final_list


def immat_error(vehicle, parc):

    for i in vehicle:
        if i["Famille"] == "Pas sur SIP2":
            if i['Vehicule'] == "Oui":
                try:
                    if i["Semaine"] == week:
                            immat_error = "vrai"
                    else : immat_error = "faux"
                except:
                    immat_error = "faux"  
            else : immat_error = "faux"
        else : immat_error = "faux"
        i.update({"Erreur Immat" : immat_error})

    return vehicle


def get_parc_window(sip2):
    
    list = []
    
    for i in sip2:
        if pd.isna(i["Date de retrait"]):
            list.append(i)

    return list