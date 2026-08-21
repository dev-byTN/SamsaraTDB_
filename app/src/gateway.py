import pandas as pd

def get_all_gateway(list) :
    
    list_gateway = []
    for i in list:
        gateway = i["serial"]
        model = i["model"][:4]

        try:
            vin = i["asset"]["externalIds"]["samsara.vin"]
        except KeyError:
            vin = None
        try : 
            status = i["connectionStatus"]["healthStatus"]
            last_connection = i["connectionStatus"]["lastConnected"]
            last_connection = last_connection[:10]
        except KeyError:
            status = None
            last_connection = None

        stat = {
            "Boitier" : gateway,
            "Model" : model,
            "VIN" : vin,
            "Status" : status,
            "Last connection":last_connection 
        }
        list_gateway.append(stat)

    return list_gateway


def get_ordered_gateway():

    list = []
    dt = pd.read_excel("../commandes 2024-2026/commandes_Boitiers.xlsx", sheet_name="Commandes")
    dt = dt.iloc[:, 2:4].to_numpy()

    for i in dt:
        model = i[0][3:7]
        gateway = i[1]

        set = {
            "Boitier" : gateway,
            "Model" : model
        }

        list.append(set)

    return list


def get_health_status(gateway, active_gateway):

    for i in gateway:
        for j in active_gateway:
            if i["Boitier"] == j["gateway"]:
                health = j["status"]
                break
            health = "Non installé"
        
        i.update({"Etat" : health})

    return gateway


def get_gateway_status():

    dt = pd.read_excel("../maintenance/rapport maintenance boitiers.xlsx")
    dt = dt.iloc[:, :5].to_numpy()
    active_gateway = []

    for i in dt:

        vehicle = i[0]
        site = i[1]
        gateway = i[2]
        version = i[3]
        status = i[4]

        set = {
            "vehicle" : vehicle,
            "site" : site,
            "gateway" : gateway,
            "version" : version,
            "status" : status
        }
        active_gateway.append(set)

    return active_gateway


def isInstalled(gateway):

    for i in gateway:
        try:
            if i["Etat"] == "Non installé":
                installed = "non"
            else: installed ="oui"
        except:
            installed = "oui"
        i.update({"Installé" : installed})
        
    return gateway




