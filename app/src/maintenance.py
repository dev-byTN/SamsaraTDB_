import pandas as pd

def get_vehicles_alerts():

    list = []

    dt = pd.read_excel("../ressource/alertes_voyant.xlsx")
    dt = dt.to_numpy()

    list = []

    for i in dt:

        atout = i[0]
        site = i[1]
        alerts = i[9]

        dic = {
            "Immatriculation" : atout,
            "Site" : site,
            "Alert" : alerts
        }
        list.append(dic)
    
    return list
    
def get_new_alerts_array(alerts):

    list = []

    for i in alerts:

        try :
            if "OFF" in i["Alert"]:
                off = "VRAI"
            else : off = "FAUX"
        except TypeError:
            off = "FAUX"

        try :     
            if "MIL" in i["Alert"]:
                mil = "VRAI"
            else: mil = "FAUX"
        except TypeError:
            mil = "FAUX"

        try:
            if "AWL" in i["Alert"]:
                awl = "VRAI"
            else: awl = "FAUX"
        except TypeError:
            awl = "FAUX"

        try:
            if "RSL" in i["Alert"] :
                rsl = "VRAI"
            else: rsl = "FAUX"
        except TypeError:
            rsl = "FAUX"
    
        dic = {
            "Immatriculation" : i["Immatriculation"],
            "Site" : i["Site"],
            "OFF" : off,
            "MIL" : mil,
            "AWL" : awl,
            "RSL" : rsl
        }
        list.append(dic)

    return list



def get_alerts_site(alerts, site):

    for i in alerts:
        for j in site:
            try :
                if i["Site"] == j["Site"]:
                    site = j["Site"]
                    break
                site = "NA"
            except TypeError:
                site = "NA"

        i.update({"Site": site})
    return alerts


def join_alerts(main, alerts):

    for i in main:
        for j in alerts:
            if i["Immatriculation"] == j["Immatriculation"]:
                off = j['OFF']
                mil = j["MIL"]
                awl = j["AWL"]
                rsl = j["RSL"]
                break
            off = "FAUX"
            mil = "FAUX"
            awl = "FAUX"
            rsl = "FAUX"
        
        i.update({"OFF" : off})
        i.update({"MIL" : mil})
        i.update({"AWL" : awl})
        i.update({"RSL" : rsl})

    return main
    
                